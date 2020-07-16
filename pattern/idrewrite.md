# Identifier Rewriting.

Recall that in patterns in `define-language` constraint checking is not performed. This means, for example, pattern `(+ e_1 e_1)` is the same as `(+ e_1 e_2)`. In order to bypass constraint checking and, more importantly, identifier name collisions while generating `Match` objects, all identifiers must be made unique. 

The algorithm proceeds in the following manner. The pattern it traversed recursively. 
* When visiting `BuildInPattern(Tag, symbol)`, get fresh identifier that includes `Tag` as a prefix. Create new `BuildInPattern` with fresh identifier.
* When visiting `Nt(prefix, symbol)`, get fresh identifier that includes `prefix`. Create new `Nt` with fresh identifier.


Todo add example?

