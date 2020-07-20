# Ellipsis Depth Checking

Motivation for ellipsis depth checking :

1. To be able to detect patterns containing incorrent ellipsis usage. For example, in pattern `(((n_1 ...) n_1) ...)` both occurences of `n_1` are under different number of ellipses (ellipsis depth) - two and one, respectively, despite the fact that both `n_1` should match the same term. Such invalid patterns should be reported during compilation.
2. To be able to generate terms, ellipsis depth of pattern variables is required.


## Algorithm

Two bits of information is needed to find out ellipsis depth of pattern variable - *number of ellipses* on the path from root to some node which is changed with each ellipsis encountered during pattern traversal; and a mapping of pattern-variables to their respective number of ellipses.

The algorithm visits nodes recursively. The following nodes may be visited.

* `Repeat(pattern)`. Increment ellipsis depth, visit `pattern`, and decrement ellipsis depth.
* `Sequence(pattern ...)` Visit child patterns recursively.
* `BuiltInPattern(kind, sym)` and `Nt(nt, sym)`. Check if `sym` is in the mapping. If not, add it to the mapping with current ellipsis depth. Otherwise, symbol is present in the mapping. Retrieve ellipsis depth from the mapping and compare it to currect ellipsis depth. If both are unequal then raise Exception.
* `InHole(pattern1, pattern2)` Recursively visit `pattern1` and `pattern2`.


