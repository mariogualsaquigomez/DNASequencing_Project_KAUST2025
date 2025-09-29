```mermaid
flowchart TD
    A[Start with a Directed Graph] --> B[Check if the Graph is Connected]
    B -->|No| H[Graph Does Not Have Eulerian Path]
    B -->|Yes| C[Count In-Degree and Out-Degree of Each Node]
    C --> D[Check Conditions]
    D -->|1. At most one node has (out-degree = in-degree + 1)] E
    E -->|AND| F[2. At most one node has (in-degree = out-degree + 1)]
    F -->|AND All Other Nodes: in-degree == out-degree| G[The Graph Has an Eulerian Path]
    D -->|Any Condition Fails| H
    G --> I[Choose Start Node]
    I -->|Node with (out-degree = in-degree + 1) if it exists| J[Find Eulerian Path Using Hierholzer's Algorithm]
    I -->|Otherwise Any Node with Outgoing Edges| J
    J --> K[Output the Eulerian Path]

    H[The Graph Does Not Have an Eulerian Path]
```