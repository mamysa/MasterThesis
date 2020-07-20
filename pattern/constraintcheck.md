# Constraint Checking

As mentioned before, Redex supports a few different forms of constraint checking; however, for the initial PyRedex implementation only "equality of terms" constraint check will be supported. For example, in pattern `(number_1 number_1)` both bound terms must be the same, that is term `(1 1)` matches the pattern but `(1 2)` does not. 

However, the `Match` object does not store multiple bindings for the same symbol and thus assignable symbols seen in the pattern have to be renamed. In the example above, the pattern could become `(number_1 number_1#1)`. Now both bound terms can be stored in the `Match` object.

Now, actual equality checks have to be inserted. Two obvious strategies could be employed here:

1. Perform constraint checking after the pattern has been matched entirely. For example, `(n_1 n_1#1 n_2 (Check n_1 == n_1#))`. The disadvantage of this strategy is that if pattern is large and something goes wrong in the beginning the rest of the pattern is still matched and lots of useless work is done. 
2. Perform constraint checking the earliest time possible. This implies that by that time both terms have to be matched. Pattern `(n_1 n_1#1 (Check n_1 == n_1#1) n_2)` is the example of such strategy. The disadvantage of this strategy is that assignable symbols under ellipsis will be checked multiple times. `(((number_1 ...) (number_1#1 ...) (check number_1 == number_1#1)) ...)`

The algorithm to be detailed below employs the second strategy.

Finally, since `Match` object now contains extra symbols such as `number_1#1` these will have to be removed after successfully matching the pattern.


## Algorithm

To be able to insert constraint-checks all symbols to end up in `Match` object have to be known. Since certain symbols will be renamed, need to maintain a mapping between old symbol and new symbol. Additionally, maintain a set to store symbols that will have to be removed. The pattern is traversed recursively. 

* `BuiltInPattern(tag, symbol)` and `Nt(nt, symbol)`. Generate a fresh symbol given template string `symbol_#`. If generated symbol is `symbol_#0` then original symbol is seen for the first time and thus remains unchanged. Otherwise, modify `BuildInPattern` and `Nt` by changing its symbol to a new one. Add new symbol to the set of the symbols to be removed. After processing the pattern, return a mapping `{tag : symbol}` if pattern is `BuildInPattern` or `{nt: symbol}` if pattern is `Nt`.

* `Literal(tag, value)` contains to no assignable symbols and thus empty list is returned.

* `Repeat(pattern)`. Recursively visit `pattern` and return its mapping. 

* `Sequence(pattern ...)`. If sequence contains no child patterns, return empty mapping. Otherwise, let `syms` be a mapping returned after visiting the first pattern. For each remaining pattern in the sequence:
	- Let `syms2` be a mapping returned after visiting the pattern.
	- Let `syms` be a result of merging `syms` and `syms2` mappings; merging will be discussed below.
	- Let `syms2merge` be a set containing pairs of symbols that have to be checked for equality obtained fter merging `syms` and `syms2` mappings. For each pair of symbols in `syms2merge` add `ConstraintCheck` node to the sequence, exactly after the current pattern. 

* `InHole(pattern1, pattern2)`. Let `syms1`, `syms2` be mappings returned after visiting `pattern1` and `pattern2`, respectively. Let `syms` be a result of merging `syms` and `syms2` mappings, and let `syms2merge` be a set containing pairs of symbols. For each pair of symbols `(s1, s2)` in the set, create `cc_i` = `ConstraintCheck(s1, s2)` node. Replace InHole pattern with `InHole(pattern1, pattern2, {cc_0 ... cc_i ... })`.

## Variable merging.
Consider pattern `(number_1 number_1#1 number_1#2)` and observe that after inserting constraint checks in the following way: `(number_1 number_1#1 (number_1 == number_1#1 ?) number_1#2 (number_1 == number_1#2 ?) (number1#1 == number_1#2 ?))` one of the comparisons it the end is superfluous since it's known that `(number_1 == number_1#1)`. Thus, while merging mappings, only one assignable symbol has to be in resulting mapping.

Given two mappings `m1 = {k_i: sym1, k_j: sym2, ...}` and `m2 = {q_i: sym, q_j: sym}`, compute `{k_0 ... k_i ... k_n}` intersection `{q_0 ... q_i ... q_n}`. If some `p_i` is in intersection, retrieve `m1[p_i]` and `m2[p_i]` and create pair out of retrieved elements. These symbols will require constraint checking. 

The resulting mapping is constructed in the following way:

* If `p_i` is in intersection, add `{p_i: m2[p_i]}` to the mapping.
* For any `k_i` that is not in intersection add `{k_i: m1[k_i]}` to the mapping.
* For any `q_i` that is not in intersection add `{q_i: m2[q_i]}` to the mapping.


