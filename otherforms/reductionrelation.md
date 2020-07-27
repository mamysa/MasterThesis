## Reduction Relation

### Grammar and Compile-Time Representation.

Subset of grammar for `reduction-relation` is as follows:

```
reduction-relation ::= (reduction-relation language domain reduction-case ...)
reduction-case     ::= (-> pattern term reduction-case-name)
domain ::= #:domain pattern
```

This form had to be modified. Example of this modification can be seen in Figure ??? below. Since PyPltRedex does not interpret Racket in any capacity, introducing `(define id expr)` form (which evaluates `expr` and assigns it to `id`) would have resulted in additional unnecessary complexity; more specifically, keeping track of forms that are not allowed to be used with `define` form such as `define-language`. Thus, `define` and `reduction-relation` were collapsed into a single form `define-reduction-relation`. In addition, use of `define` form to define reduction-relations seems to be inconsistent with respect to `define-language` and `define-metafunction` forms.

```
(define red (reduction-relation MyLanguage 
	; omitted
	))

(define-reduction-relation red MyLanguage 
	; omitted
)
```

Modified grammar for `define-reduction-relation` can be seen below.

```
define-reduction-relation ::= (define-reduction-relation reduction_name language domain reduction-case ...)
reduction-case     ::= (-> pattern term)
domain ::= #:domain pattern
```

`domain` optional parameter provides contract for reduction relation. When `reduction-relation` is applied to a term, it has to satisfy the contract; that is the term must match provided pattern otherwise it is an error. Similarly, after applying reduction relation to the term, resulting term(s) also have to sastisfy said contract; that is each term has to match the pattern provided by `domain`.

Grammar defined above leads to the following compile-time representation:

```py
class DefineReductionRelation(TopLevelForm):
    class ReductionCase:
        def __init__(self, pattern, termtemplate, name):
            self.pattern = pattern
            self.termtemplate = termtemplate
            self.name = name

    def __init__(self, name, languagename, domain, reductioncases):
        self.name = name
        self.languagename = languagename
        self.reductioncases = reductioncases
        self.domain = domain
```

### Preprocessing

Domain pattern:
NtRewriter -> IdRewriter -> InHoleChecker -> AssignableSymbolExtractor


Pattern in reduction-case:
NtRewriter -> -> InHoleChecker -> ConstraintCheckInserter -> AssignableSymbolExtractor

Term-template in reduction-case
EllipsisDepthChecker -> MetafunctionApplicationRewriter.


### Application Algorithm.
Application of reduction relation on the term is essentially an application of each individual reduction case on the term. Given term `t`:

* If domain pattern `d` is present, match `t` against `d`. If there are no matches, that means contract is not satisfied and error should be raised.
* Create set `T = {}` that stores terms after applying reduction-cases to `t`.
* Then, for each reduction case `rc = (pattern, termtemplate, name)` in reduction relation, match `pattern` against `t`. Let `M` be the set of resulting matches. Then for each `m in M`:
	1. Generate term `t_prime` with `termtemplate(m)`.
	2. Match `t_prime` against pattern `d`. If there no matches, raise error.
	3. T = T union {t_prime}
* Return set `T`.

### Code Generation.

Algorithm above leads to the following code being generated. For reduction-case and for reduction-relation

```py
def genReductionCase(pattern, termtemplate, name, domain):
	patternproc = codegen(pattern)
	termtemplateproc = codegen(termtemplate)
	reductioncaseproc = SymGen()
	emit(
	"""
	def {$reductioncaseproc}(T, term):
	 matches = {$patternproc}(term)
	 if len(matches) != 0:
	   for match in matches:
		 termprime = {$termtemplate}(match)
		 domaincheckmatches = {$domain}(termprime)
		 if len(domaincheckmatches) == 0:
		   raise Exception(reduction-relation {}: term reduced from {} to {} via rule {} and is outside domain)
		 T = T.union(termprime)
	""")

	return reductioncaseproc
```

```py
def genDefineReductionRelation(reductionrelation):
	emit( "T = set()" )
	for reductioncase in reductionrelation:
		reductioncaseproc = codegen(reductioncase)
		emit( '{$reductioncaseproc}(T, term)' )
	emit( 'return T' )
```

