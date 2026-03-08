"""Crush-Dotsy Autonomous Agent Coordination.

This module enables Dotsy to coordinate with Crush CLI as an autonomous agent,
allowing them to work together on complex tasks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

from dotsy.core.tools.builtins.crush import CrushCLI, CrushConfig


class AgentRole(StrEnum):
    """Role of an agent in the coordination."""

    ORCHESTRATOR = auto()  # Dotsy coordinates
    WORKER = auto()  # Crush executes
    COLLABORATOR = auto()  # Both work together


class TaskStatus(StrEnum):
    """Status of a coordinated task."""

    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class CoordinatedTask:
    """A task coordinated between Dotsy and Crush."""

    id: str
    description: str
    role: AgentRole
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None
    error: str | None = None
    metadata: dict[str, Any] | None = None


class CrushDotsyCoordinator:
    """Coordinates tasks between Dotsy and Crush CLI."""

    def __init__(
        self,
        crush_config: CrushConfig | None = None,
        auto_approve: bool = False,
    ) -> None:
        self.crush_cli = CrushCLI(config=crush_config)
        self.auto_approve = auto_approve
        self.tasks: dict[str, CoordinatedTask] = {}
        self._task_counter = 0

    def is_available(self) -> bool:
        """Check if Crush CLI is available for coordination."""
        return self.crush_cli.is_available()

    def create_task(
        self,
        description: str,
        role: AgentRole = AgentRole.WORKER,
        metadata: dict[str, Any] | None = None,
    ) -> CoordinatedTask:
        """Create a new coordinated task."""
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"

        task = CoordinatedTask(
            id=task_id,
            description=description,
            role=role,
            metadata=metadata or {},
        )
        self.tasks[task_id] = task
        return task

    async def execute_task(
        self,
        task: CoordinatedTask,
        context: dict[str, Any] | None = None,
    ) -> CoordinatedTask:
        """Execute a coordinated task."""
        task.status = TaskStatus.IN_PROGRESS

        try:
            if task.role == AgentRole.WORKER:
                # Crush executes the task
                result = await self._execute_with_crush(task, context)
                task.result = result
                task.status = TaskStatus.COMPLETED

            elif task.role == AgentRole.ORCHESTRATOR:
                # Dotsy orchestrates, possibly delegating to Crush
                result = await self._orchestrate_task(task, context)
                task.result = result
                task.status = TaskStatus.COMPLETED

            elif task.role == AgentRole.COLLABORATOR:
                # Both work together
                result = await self._collaborate_on_task(task, context)
                task.result = result
                task.status = TaskStatus.COMPLETED

        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED

        return task

    async def _execute_with_crush(
        self,
        task: CoordinatedTask,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Execute task using Crush CLI."""
        if not self.crush_cli.is_available():
            raise RuntimeError("Crush CLI is not available")

        # Prepare the task for Crush
        task_description = task.description
        if context:
            task_description += f"\n\nContext: {json.dumps(context, indent=2)}"

        # Run with Crush
        returncode, stdout, stderr = self.crush_cli.run_command(
            ["--yolo" if self.auto_approve else "", task_description],
            timeout=600,
        )

        if returncode != 0:
            raise RuntimeError(f"Crush failed: {stderr or stdout}")

        return stdout

    async def _orchestrate_task(
        self,
        task: CoordinatedTask,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Orchestrate task execution (Dotsy coordinates, may delegate to Crush)."""
        # Dotsy analyzes the task and decides how to proceed
        # For now, we'll delegate to Crush
        return await self._execute_with_crush(task, context)

    async def _collaborate_on_task(
        self,
        task: CoordinatedTask,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Collaborate on task (both Dotsy and Crush contribute)."""
        # This is a more complex workflow where both agents contribute
        # For now, we'll execute with Crush and let Dotsy post-process
        crush_result = await self._execute_with_crush(task, context)

        # Dotsy can analyze and enhance the result
        # This is a placeholder for future enhancement
        return crush_result

    def get_task(self, task_id: str) -> CoordinatedTask | None:
        """Get a task by ID."""
        return self.tasks.get(task_id)

    def get_active_tasks(self) -> list[CoordinatedTask]:
        """Get all active (non-completed) tasks."""
        return [
            t for t in self.tasks.values()
            if t.status not in (TaskStatus.COMPLETED, TaskStatus.CANCELLED)
        ]

    def get_task_history(self) -> list[CoordinatedTask]:
        """Get all tasks in history."""
        return list(self.tasks.values())

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        task = self.tasks.get(task_id)
        if task and task.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS):
            task.status = TaskStatus.CANCELLED
            return True
        return False

    def get_context_summary(self) -> dict[str, Any]:
        """Get a summary of the current coordination context."""
        crush_context = self.crush_cli.get_context()
        return {
            "crush_available": self.is_available(),
            "crush_context": crush_context,
            "active_tasks": len(self.get_active_tasks()),
            "total_tasks": len(self.tasks),
            "completed_tasks": sum(
                1 for t in self.tasks.values()
                if t.status == TaskStatus.COMPLETED
            ),
            "failed_tasks": sum(
                1 for t in self.tasks.values()
                if t.status == TaskStatus.FAILED
            ),
        }


class AgentCommunicationProtocol:
    """Protocol for communication between Dotsy and Crush.

    This defines a simple message format for agent-to-agent communication.
    """

    @staticmethod
    def create_message(
        sender: str,
        recipient: str,
        message_type: str,
        content: Any,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a message for agent communication."""
        return {
            "sender": sender,
            "recipient": recipient,
            "type": message_type,
            "content": content,
            "metadata": metadata or {},
            "timestamp": str(Path.cwd()),  # Could use datetime
        }

    @staticmethod
    def parse_message(message: dict[str, Any]) -> dict[str, Any]:
        """Parse and validate a message."""
        required_fields = ["sender", "recipient", "type", "content"]
        for field in required_fields:
            if field not in message:
                raise ValueError(f"Missing required field: {field}")
        return message

    @staticmethod
    def create_task_request(
        task_id: str,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a task request message."""
        return AgentCommunicationProtocol.create_message(
            sender="dotsy",
            recipient="crush",
            message_type="task_request",
            content={
                "task_id": task_id,
                "description": description,
                "parameters": parameters or {},
            },
        )

    @staticmethod
    def create_task_response(
        task_id: str,
        success: bool,
        result: Any | None = None,
        error: str | None = None,
    ) -> dict[str, Any]:
        """Create a task response message."""
        return AgentCommunicationProtocol.create_message(
            sender="crush",
            recipient="dotsy",
            message_type="task_response",
            content={
                "task_id": task_id,
                "success": success,
                "result": result,
                "error": error,
            },
        )


# Singleton instance for easy access
_coordinator: CrushDotsyCoordinator | None = None


def get_coordinator(auto_approve: bool = False) -> CrushDotsyCoordinator:
    """Get the global coordinator instance."""
    global _coordinator
    if _coordinator is None:
        _coordinator = CrushDotsyCoordinator(auto_approve=auto_approve)
    return _coordinator


def reset_coordinator() -> None:
    """Reset the global coordinator instance."""
    global _coordinator
    _coordinator = None
