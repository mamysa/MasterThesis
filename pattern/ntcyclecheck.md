# Non-Terminal Cycle checking.

PltRedex disallows language definitions such as ones in Figure below. 

```
(define-language L
	(e ::= n (e e))
	(n ::= p (n n) number)
	(p ::= e (p p) real))

```

The problem with the language above (aside from it being completely useless) is a cycle of non-terminals `[n, p, e]`. It is clear that in order to match `e`, `n` has to matched first. To match `n`, `p` has to matched first. To match `p`, `e` has to be matched first. This results in infinite recursion. Thus, such cases need to be reported.

To detect such cycles, `define-language` needs to be interpreted as directed graph and some cycle-detecting algorithm must be used. Graph is constructed in the following manner.

* For each non-terminal definition, create vertex in the graph labelled with non-terminal symbol `p`.
* For each pattern in non-terminal definition, if pattern is `Nt(q)` then create edge `p->q`.

For language above this graph would look like this:

For cycle detection, depth-first-search is employed. Vertices in the graph can be assigned one of three colors:
* *White* meaning the vertex hasn't been visited before. All vertices are initially assigned this color.
* *Grey* meaning successors of the vertex `v` are still being visited. When `v` is visited for the first time, `color(v)` becomes *Grey*.
* *Black* meaning all successors of the vertex `v` have been explored. After visiting all successors `color(v)` becomes *Black*.

Vertex coloring allows for detection of cycles; more specifically, if during depth-first-traversal vertex `v` is encountered with `color(v)=Grey`, this means that there's a *back-edge* in dfs-tree. (expand). That is, back-edge (u,v) connects vertex `v` to its predecessor in depth-first-search tree `u`. Once such cycle is found, the error is reported and compilation aborts.

To report a path of non-terminals that make up the cycle, a path of non-terminals has to be maintained. The path can be represented as a stack. The vertex is added to the stack when it changes color to `Grey` and removed from the stack when it changes color to `Black`. Pseudocode for depth-first-traversal and cycle reporting can be seen below.

```
def reportcycle(path, v):
	idx = path.indexof(v)
	cyclepath = path[idx:] + [v]
	raise CompilationError(nt cycle {}.format(cyclepath))

def visit_vertex(v, V, path):
	if v.color == White:
		path.append(v)
		v.color = Grey 
		for successor in v.successors:
			self.visit(successor, V, path)
		v.color = Black
		V = V.union(v)
		path.pop()
	if v.color == Discovered:
		reportcycle(path, v)
```

Since resulting non-terminal graphs may be disjoint, we need to keep track of visited vertices during traversal. Let `V` be a set of vertices whose `color(v)=Black`. Thus, every time vertex `v` changes its color to `Black`, `V = V union { v } `. Let `U` be a set of vertices whose `color(u)=White`; that is, it initially contains all the non-terminals. The algorithm proceeds as follows:

* Pick random vertex `u` from set `U`. Create empty set `V`. Starting from `u` perform depth-first-search as described above. Compute set difference - `U = U-V`.
* Continue until `U` is empty.

Pseudo-code for this procedure can be seen below.

```
def visit_graph(graph):
	U = set(self.nts)
	while len(U) != 0:
		V = set()
		self.visit(U.get_random_element(), V, [])
		U = U - V

```

Note that the described algorithm does not report all the cycles in the graph but the first one it manages to find.
