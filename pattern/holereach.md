# Hole Reachability.

Recall that pattern `InHole(pattern1, pattern2)` requires `pattern1` to match exactly one `hole` term. The main problem is counting a number of holes matched by non-terminal symbols of the language. Consider the language `MatchesManyHoles` listed below.

```
(define-language MatchesManyHoles
	(n ::= number)
	(P ::= E (n ... E ...))
	(E ::= (+ E P) (+ n E) hole))
```

To compute value for non-terminal `E` analysis of pattern `(+ E P)` is required but the vallue of `E` is not yet known. Moreover, computing a single value that represents number of holes in insufficient; pattern `(E ...)` may match zero or many holes. Thus, a *minimum* and *maximum* number of holes matched by some pattern must be computed. 

This problem can be reduced to graph traversal. All explicit non-terminal references are replaced with edges to expressions said non-terminal matches. 

## Graph Modelling.

Graph consists of two parts - *outer-nodes* and *inner-nodes*.

Outer-nodes are a stand-in for the pattern and come in four different varieties:

* `Sequence` representing pattern-sequences.
* `Repeat` representing ellipses.
* `LeafHole` that represents pattern `hole`.
* `LeafNotHole` that represents any other pattern except `InHole(pattern1, pattern2)`.

Inner-nodes are stored in `Sequence` and `Repeat` outer-nodes and act as non-terminal references. Each inner-node has a set of outer-node successors pointing to a set of expressions that the non-terminal matches. 

Graph for language defined above can be seen in the following figure:

TODO

## Graph Construction.

Constructing the graph involves two stages: 

1. Creation of outer nodes for each top-level pattern such as `(+ E P)` or `hole`.
2. Creation of inner nodes and edges from inner to outer nodes. If outer node is a `Sequence` and it contains other sequences or ellipses, additional creation of outer-nodes will be required. 

## Creation of outer nodes

Need to maintain a mapping `M` between patterns in non-terminal definition. For each non-terminal definition `N` let `E_N = {}` be a set storing top-level non-terminal references. For example, in the language described above for non-terminal definition `P` the only such reference is `E`.

Each non-terminal definition `N` is visited and we may come across the following patterns.

* `p = BuiltInPat(kind, symbol)`. If kind is `Hole` then `n = LeafHole` node is created.  Otherwise, `n = LeafNotHole` node is created. Thus, `M = M union {(p, n)}`.
* `p = Nt(nt, sym)`. This means that `N` is also `nt` and thus all expressions in non-terminal definition of `nt` should also be reachable from any inner-node that reaches expressions in `N`. Thus, `E_N = E_N union {nt}`.
* `p = InHole(pattern1, pattern2)`. Raise compilation error and quit. This, however, is not actual behaviour of the PltRedex. (TODO explain why we handle it differently?)
* `p = PatternSequence(pattern ...)`. If length of `p` is zero, then `n = LeafNotHole`, otherwise `n = Sequence`. Thus, `M = M union {(p, n)}`.

Note that creating multiple `LeafHole` or `LeafNotHole` nodes is not necessary and existing nodes of these kinds can be reused. This means that the graph may have at most two leaf nodes.

## Creation of inner-nodes and edges.

The only top-level pattern kind that may contain inner nodes at this point is `Sequence`.



