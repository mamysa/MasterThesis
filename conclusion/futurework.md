## Ellipsis Determinism

In Chapter < Pattern codegen > an algorithm for deterministic matching of patterns under ellipsis was described but careful reader might notice the report doesn't describe how such patterns are made deterministic. In fact, PyPltRedex provides a transformation pass called `EllipsisMatchModeRewriter` that analyzes patterns under ellipses and decides if given ellipsis can be matched deterministically but current algorithm is flawed and doesn't work correctly for all patterns. 


## `define-judgment-form`  and `judgment-holds`

PyPltRedex doesn't implement `define-judgment-form` that allows for specification of type-inference rules and `judgment-holds` that given a term attempts to apply specified typing rules.  

## `define-metafunction` and `define-reduction-relation` pattern merging.

Algorithms for application of reduction-relation and metafunctions match each pattern separately. However, it may be the case that patterns in reduction-cases are similar and bind terms to same identifiers in the same position within the pattern.
```
(M_1  (in-hole P x (+ n_1 n_2)))
(M_1  (in-hole P n (- n_1 n_2)))
```
Two patterns above are an example - both patterns contain pattern-variable `M_1` in the first position within the sequence. This means at this point there needs to be a single `Match` object containing `M_1`. Since `in-hole` patterns are different, after matching `M_1` `Match` object can be copied to contain terms matches by each `in-hole`. Diagram can be seen below - 

TODO

Furthermore, the first pattern in both `in-hole` patterns is the same - `P`. Since both `in-hole` patterns are at the second position within respective pattern sequences, instead of using multiple term traversals to find child terms matching `(+ n_1 n_2)` and `(- n_1 n_2)`, one travesal would be sufficient. This could be done by introducing a new pattern, say, `InHoleMulti(pattern1, pattern2 ...)` that accepts multiple patterns. Diagram for this can be seen below:

TODO

However, since since matches may have been split before, this introduces additional complexity of `Match` object management.
