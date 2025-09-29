```mermaid
graph TD
    A[Start] --> B{Input: Directed Graph G};
    B --> C{1. Check Preconditions};
    C --> C1{"Is the graph portion with edges
    strongly connected?"};
    C1 -- No --> Z[End: No Eulerian Path];
    C1 -- Yes --> D[Calculate in-degree and out-degree for each vertex];
    D --> E{Count vertices where in-degree != out-degree};
    E --> F{How many such vertices?};
    F -- "Zero" --> G["Condition Met for Eulerian Circuit
    (Path is a Circuit)"];
    F -- "Two" --> H{"One vertex with out-degree = in-degree + 1?
    AND
    One vertex with in-degree = out-degree + 1?"};
    F -- "More than Two" --> Z;
    H -- No --> Z;
    H -- Yes --> I[Condition Met for Eulerian Path];
    G --> J{2. Find Starting Node};
    I --> J;
    J --> K{Is it a circuit (zero mismatched degrees)?};
    K -- Yes --> L[Pick any vertex as the start node];
    K -- No --> M["Start node is the vertex where
    out-degree = in-degree + 1"];
    L --> N{3. Find the Path};
    M --> N;
    N --> O["Initialize an empty 'path' stack
    and an empty 'eulerian_path' list"];
    O --> P[Push the start node onto the 'path' stack];
    P --> Q{While the 'path' stack is not empty};
    Q -- True --> R[Let u = the vertex at the top of the 'path' stack];
    R --> S{Does 'u' have any unvisited outgoing edges?};
    S -- Yes --> T["Select an unvisited edge (u, v)
    Mark edge as visited
    Push 'v' onto the 'path' stack"];
    T --> Q;
    S -- No --> U["Pop 'u' from the 'path' stack
    Add 'u' to the front of the 'eulerian_path' list"];
    U --> Q;
    Q -- False --> V[The 'eulerian_path' list now holds the complete path];
    V --> W[End];
```
When you commit this to a GitHub repository and view the file, it will automatically render into the flowchart diagram.