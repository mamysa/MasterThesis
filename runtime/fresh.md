## Fresh Variable Generation.

PltRedex provides a very convinient form `(variables-not-in t p)`. Term `p` is expected to contain a single variable `v` such as `(term a)`. Given term `t`, `variables-not-in` form produces a term containing fresh variable `v_out` with prefix `p_out` and some suffix `s_out` such that there's no variable `v_prime` in `t` with `v_out = v_prime`; or `v_out not in Variables(t)` where `Variables(t)` is the set of all variables in `t`. Suffix `s_out` may contain only digits or otherwise be empty. 

For example, variable `abc1xyz123` is decomposed into prefix `abc1xyz` and suffix `123`.

### Algorithm.
* Initialize an empty dictionary.
* For each `v_prime in Variables(t)`, try to decompose `v_prime` into `p_prime` and `s_prime` interpreted as a number. 
	* If such decomposition is possible, insert `(p_prime, s_prime)` into the dictionary. If `p_prime` is not in the dictionary, initialize it to be an empty list and append `s_prime` to it.
	* Otherwise, insert `(v_prime, -1)` into the dictionary `d`. If `v_prime` is not in the dictionary, initialize it to be an empty list and append string -1 to it. Special value of -1 is used to indicate that `v_prime` does not have a suffix.
* Decompose `v` into prefix `p` and suffix `s`.
	* If decomposition is not possible, check if `v` is in dictionary `d` and return `Variable(v)` if it is not - this means term `v` is not in Variables(t).
	* if decomposition is possible, check if `p` is in dictionary `d` and return `Variable(v+s)` if it not. Additionally, check if suffix `s` is in `d[p]`. If it is not, return `Variable(v+s)`. This is done to return `a00` given `Variables(t) = {a, a0}` and `v=a00`, for example. Otherwise, let `v=p`.
* Otherwise, algorithm resorts to searching for unique suffix by interpreting each suffix in `d[v]` as a number. Let `N` be list containing prefixes interpreted as a number and sorted in ascending order.  The goal is to find smallest number `i > 0` that is not in `N`. If first `N[0]` is not `-1`, then `v` is not in `Variables(t)` and is already fresh. Return `Variable(v)`.
* Initialize `i=1` and `j=1`. `N[0]` is -1. Let `n` be the length of the list `N`. While `j<n`:
	* If `i < N[j]` return `Variable(v+i)`.
	* If `i > N[j]` then increment `j` by one. This case only happens when 0 is in `N`
	* If `i = N[j]` then increment both `i` and `j` by 1.

* The end of the list is reached and `Variable(v+i)` is returned.

This completes the description of the fresh variable generation.

