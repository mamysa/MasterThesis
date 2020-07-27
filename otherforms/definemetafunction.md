## Define-Metafunction

Supported subset of `define-metafunction` grammar is as follows:

```
(define-metafunction language-name
  metafunction-contract
  metafunction-case ...)

metafunction-contract =	id : pattern-sequence ... -> pattern 
metafunction-case =  [(name pattern ...) term] 
```

A metafunction is a function on terms. The define-metafunction form builds a metafunction according to the pattern and right-hand-side expressions. The first argument indicates the language used to resolve non-terminals in the pattern expressions. Each of the rhs-expressions is implicitly wrapped in term. (TODO rewrite this)

The contract is matched against every input and output of the metafunction and, if the match fails, an exception is raised. Unlike PltRedex, which supports constraint checks on domain when patterns are suffixed with identifier (i.e. in `(number_1 number number number_1)` both terms matching metavariable `number_1` must be equal), PyPltRedex assumes all metavariables are unique. 

Exception is also raised when 

1. Term doesn't match any metafunction case.
2. Matching the term results in multiple matches and terms created using these matches are not all equal. 
TODO example (non-det (n_1 ... n_2 ...)) -> ,(+ (term (n_1 ...)))
 
This results in the following compile-time representation:

`DefineMetafunction(languagename, contract, metafunctioncases)`.
`MetafunctionContract(name, pattern_1, pattern2)` where `pattern1` is `(id pattern-sequence ...)` and created implicitly, and `pattern2` is the pattern after the arrow.
`MetafunctionCase(pattern, termtemplate)`.

### Preprocessing
Before applying transformations, have to ensure that every pattern in metafunction-case begins with `id`. This is done by iterating over each case, retrieving first element `e` from the sequence, ensuring Tag(e) is `Variable` and `Value(e)` = `id`. Otherwise, raise error and about compilation.

Domain and co-domain patterns:
NtRewriter -> IdRewriter -> InHoleChecker -> AssignableSymbolExtractor

Pattern in reduction-case:
NtRewriter -> -> InHoleChecker -> ConstraintCheckInserter -> AssignableSymbolExtractor

Term-template in reduction-case
EllipsisDepthChecker -> MetafunctionApplicationRewriter.


### Metafunction Application Algorithm.
Given term `t` and some metafunction:

* Match `t` against domain pattern `p_domain`. If resulting set of matches is empty, raise Exception.
* For each metafunction-case `mc`, apply `mc` to the term `t`. If it successfully returns term `t_prime`, match `t_prime` against co-domain pattern `p_codomain`. If resulting set of matches is empty, raise Exception.
* If none of metafunction-cases were matched, raise Exception.

Given term `t` and metafunction-case `mc=(pattern, term-template)`:

* Apply matching procedure `pattern(t)`. If resulting set of matches is empty, exit.
* Create empty set `T = {}`. For every match `m` in the set, generate a term `t_prime = term-template(m)` and `T = T union t_prime`.
* For each pair of terms `t_prime_1` and `t_prime_2`, ensure that both terms are equal. If they are not, raise Exception.
* Pick random term `t_prime` from T and return it.

### Code Generation

```
#def mfcase(argterm):
#  tmp0 = matchfunc(argterm)
#  tmp1 = []
#  if len(tmp0) == 0:
#    return tmp1 
#  for tmp2 in tmp0:
#    tmp3 = termfunc(tmp2)
#    tmp4 = tmp1.append(tmp3)
#  tmp5 = aretermsequalpairwise(tmp1)
#  if tmp5 != True:
#    raise Exception('mfcase 1 matched (term) in len(tmp{i}) ways, single match is expected')
#  tmp6 = tmp1[0]
#  return tmp6
```

```
#def mf(argterm):
#  tmp0 = domaincheck(argterm)
#  if len(tmp0) == 0:
#    raise Exception('mfname: term is not in my domain')
#  { foreach reductioncase
#  tmp{i} = mfcase(term)
#  if len(tmp{i}) == 1:
#    tmp{j} = tmp{i}[0]
#    tmp{k} = codomaincheck(tmp{j})
#    if len(tmp{k}) == 0:
#      raise Exception('mfname: term not in my codomain')
#    return tmp{j}
#  }
#  raise Exception('no metafuncion cases matched for term')
```
