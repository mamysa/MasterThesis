# DefineLanguage

## Grammar and Compile-time Representation.

Recall that languages are defined using `define-language` form that has the following grammar. Language definition consists of one or more non-terminal definitions which are just a tuple consisting of non-terminal symbol and one or more patterns the non-terminal symbol matches.

```
define-language ::= (define-language language-name non-terminal-definition ... +)
non-terminal-definition ::= (non-terminal-name ::= pattern ... +)
```

Compile-time representation of `define-language` follows the grammar defined above closely. More specifically, 

* `DefineLanguage(name, ntdef)` represents `define-language` form. 
* `NtDefinition(sym, patterns)` represents `non-terminal-definition` inside `define-language`

## Preprocessing.

Using transformation / analysis passes described in Chapter **pattern**, each pattern in non-terminal definition goes through the following transformations.

NtRewriter -> IdRewriter -> NtCycleChecker -> HoleReachabilitySolver -> AssignableSymbolExtractor

## Code Generation
Code generation for each pattern in the `non-terminal-definition` takes place as described in `codegen` section in `pattern` chapter. The only thing that is left out is generation of Is-A procedures for every non-terminal definition.

###Is-A procedures for non-terminals.

```py
(define-language Lc
  (e ::= (e e) (+ e ...) (if e e e) v)
  (v ::= (λ x e) n b x)
  (n ::= number)
  (b :: boolean)
  (x ::= variable-not-otherwise-mentioned))
```

For each pattern defined by non-terminal, first generate matching procedure and top-level matching procedure, call top-level matching procedure and verify a list of matches is not empty. If it is not, immediately return `True`. Otherwise, try matching the next pattern in the list. If none of the patterns match the term, return False.

Figure below shows sample `is-a` procedure for non-terminal `e`.

```py
def isa_e(term):
	if match('(e e)', term):     return True
	if match('(+ e ...)', term): return True
	if match('(if e e e)', term): return True
	if match('v', term):          return True
	return False
```

Such generated code also shows the need for non-terminal cycle checking in [CHAPTER XXX]. For example given grammar the following `is-a` procedures will be generated for both non-terminal symbols. Infinite-recursion!

```
(x : n variable-not-otherwise-mentioned)
(n : xnumber)

def isa_x(term):
	if match('n', term):     return True
	if match('variable-not-otherwise-mentioned', term):     return True
	return False

def isa_n(term):
	if match('x', term):     return True
	if match('number', term):     return True
	return False
```
