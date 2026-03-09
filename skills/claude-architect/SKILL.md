---
name: claude-architect
description: System design and architecture expert for planning scalable, maintainable software systems
license: MIT
compatibility: Works with any software architecture or design task
metadata:
  author: Dotsy Community
  version: 1.0.0
  category: architecture
allowed-tools: []
user-invocable: true
---

# Claude Architect

This skill provides expert software architecture and system design guidance, leveraging Claude's strengths in high-level reasoning and system thinking.

## When to Use

- Designing a new application or service from scratch
- Planning microservices architecture
- Making technology stack decisions
- Refactoring legacy systems
- Scaling existing applications
- API design and documentation

## Capabilities

### System Design
- **Architecture Patterns**: Recommends appropriate patterns (MVC, microservices, event-driven, etc.)
- **Component Design**: Breaks down systems into manageable components
- **Data Flow**: Maps out how data moves through your system
- **Integration Strategy**: Plans third-party service integrations

### Technology Selection
- **Framework Comparison**: Evaluates pros/cons of different frameworks
- **Database Selection**: Recommends SQL vs NoSQL based on needs
- **Infrastructure**: Suggests deployment and hosting strategies
- **Tool Recommendations**: IDEs, CI/CD, monitoring, etc.

### Scalability Planning
- **Horizontal vs Vertical**: Growth strategy recommendations
- **Caching Strategy**: Redis, CDN, application-level caching
- **Load Balancing**: Distribution strategies
- **Database Scaling**: Sharding, replication, read replicas

### API Design
- **RESTful Principles**: Resource design, HTTP methods, status codes
- **GraphQL Schemas**: Type definitions, resolvers, queries
- **API Documentation**: OpenAPI/Swagger specifications
- **Versioning Strategy**: Backward compatibility planning

### Security Architecture
- **Authentication Systems**: OAuth, JWT, session management
- **Authorization Models**: RBAC, ABAC, permissions
- **Data Protection**: Encryption, hashing, key management
- **Threat Modeling**: Identifying and mitigating risks

## Usage

Invoke with `/claude-architect` and describe:
1. Your project goals and requirements
2. Current constraints (budget, team size, timeline)
3. Any existing systems or technical debt
4. Expected scale and growth projections

## Example

```
/claude-architect
I need to design a real-time chat application for 100K concurrent users.
Requirements:
- End-to-end encryption
- Message history
- File sharing
- Mobile and web clients
Budget: Startup phase, need cost-effective solution
```

## Output Format

Architecture documents include:
- 📐 **Architecture Diagram**: Component overview and relationships
- 🛠️ **Tech Stack**: Recommended technologies with justification
- 📊 **Data Model**: Database schema and data flow
- 🔐 **Security Considerations**: Threat model and mitigations
- 📈 **Scaling Strategy**: Growth plan and bottlenecks
- ⚖️ **Trade-offs**: Decisions made and alternatives considered
