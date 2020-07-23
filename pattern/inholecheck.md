# InHole Checking

Having computed `min/max` numbers for each non-terminal in the language, now the question of whether `pattern1` in pattern `InHole(pattern1, pattern2)` actually matches exactly one hole. Doing so involves two stages: 

1. Locating `InHole(pattern1, pattern2)` in the top-level pattern.
2. Checking if `pattern1` matches exactly one hole. Since `pattern1` doesn't necessarily have to be a non-terminal, so extra work will have to be required.


## Checking pattern for number of holes.

Assuming `InHole(pattern1, pattern2)` pattern has already found, `pattern1` has to be visited recursively. One of the following nodes may be visited.

* p = BuiltInPattern(tag, sym) - if tag is `hole` then `min_p = One, max_p = One`, otherwise `min_p = Zero, max_p=Zero`.

* `p = Nt(nt, ntsym)`. Read appropriate annotation from non-terminal definition in `define-language` and return values.

* `p = Lit(kind, value)`. min_p = Zero, max_p = Zero.

* `p = InHole(pattern1, pattern2)`. Return `min_p = Zero, max_p = Zero`, this seems to be default PltRedex behaviour.

* `p = Repeat(p2)`. Recursively visit the `pattern` obtaining `min_p2`, `max_p2`. The logic for Repeat is identical to the one used in **Hole Reachability**; that is:
	- `min_n = Zero`
	- `max_p = Many if max_p2 = One or max_p2 = Many`
	- `max_p = Zero` otherwise

* `p = Sequence(p_0 p_i ... p_n)`. Initially, min_p, max_p = Unitialized. Then, min_p = \sum{p_i in p} min_p_i. To obtain min_p_i, p_i has to be recursively visited.

TODO include pseudocode?

## Locating In-Hole

Locating `InHole(pattern1, pattern2)` is trivial task.

## Example ...?
TODO
