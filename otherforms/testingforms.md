## Additional Testing Forms

PyPltRedex provides a number of additional forms that provide testing functionality. The goal is to be able to run individual components of PyPltRedex such as pattern matcher and term generator and compare results against expected ones. 

### redex-match-assert-equal

This form is based on `redex-match` form provided by PltRedex but additionally it also requires a list of matches to compare results of matching against. The grammar for this form can be seen below.

```
redex-match-assert-equal = (redex-match-assert-equal language pattern term-template match-list)
match-list = ( match ... )
match = (match bindings ...)
bindings = (bind ident term-template)
```

This form accepts the term, matches it against a pattern with non-terminal symbols from `language`, and resulting list of matches is compared against expected list of matches. Order of expected matches in the list is important. Exception is raised if 

1. Lengths of expected list and list produced by the matcher are not the same.
2. Two matches at position i in both lists are not the same; that is, given two matches `m_1` and `m_2` Sym(m_1) intersection Sym(m_2) = Sym(m_1) ^ Sym(m_1) intersection Sym(m_2) = Sym(m_2) (all symbols that are present in m_1 are also present in m_2) and for any symbol `s` in Sym(m_1), Term(m_1, s) = Term(m_2, s) (terms bound to `s` must be identical).

Match is essentially a list of tuples containing pattern-variable and term-template.

Example of usage of this form can be seen below: 

```
(redex-match-assert-equal Lc (n_1 ... n_2 ...) (term (1 2 3))
  ((match (bind n_1 ())      (bind n_2 (1 2 3)))
   (match (bind n_1 (1))     (bind n_2 (2 3)))
   (match (bind n_1 (1 2))   (bind n_2 (3)))
   (match (bind n_1 (1 2 3)) (bind n_2 ()))))
```

Compile-time representation of this form is straight-forward:

* `RedexMatchAssertEqual(languagename, pattern, termtemplate, matchlist)`
* `Match(dictionary)`. Dictionary stores the mapping between pattern-variable and term-template.

#### Preprocessing patterns.
TODO

####Code Generation.

Code generation involves three steps: 

1. Generating a a list of expected matches.
2. Generating matching procedure and generating a term that will be matched against the pattern.
3. Compare expected matches against results obtained after matching.

Code snippet below demonstrates how list of matches is created. For each match, generate a fresh variable and store it in the list. Emit code that assigns new `Match` instance to the fresh variable. For each symbol and term-template in the match, generate term-creation procedure for term-template. Emit code that calls term-creation procedure and adds the term to the `Match` instance with appropriate symbol.

```
def gen_matches(matches):
	symgen = Symgen()
	processed = []
	for match in matches:
		matchvar = Symgen()
		emit( '${matchvar} = Match()' )
		processed.append(matchvar)

		for symbol, termtemplate in match.bindings:
			termtemplateproc = codegen(termtemplate)
			emit(
			"""
			term = ${termtemplateproc}(Match())
			${matchvar}.addKey({$symbol})
			${matchvar}.addtoBinding({$symbol}, term)
			"""
			)
		emit('expected = ${proccessed}')
	return 'expected'
```
Then, generate code for the pattern and termtemplate, emit code that first calls term-template building procedure to obtain the term, call pattern matching procedure that obtains a list of matches and then call `assert_compare_match_lists` with expected and actual lists.

Code generation for `redex-match-assert-equal` procedure is finished and the procedure has to be called. 

```
def gen_redexmatchassertequal(languagename, pattern, termtemplate, expectedmatches):
	patternproc = codegen(pattern)
	termproc    = codegen(termtemplate)

	procedurename = beginprocedure()
	expectedsym = gen_matches(expectedmatches)
	emit( 'term   = {$termproc}( Match()  )
	emit( 'actual = {$patternproc}(term)' )
	emit( 'assert_compare_match_lists(${expectedsym}, actual)' )
	endprocedure()
	emit({$procedurename}())
```

### term-let-assert-equal

Given a list of pattern-variable assignments, replaces all pattern-variables in term-template with provided terms and then asserts that resulting term is equal to the expected one. The grammar for this can be seen below. 

```
term-let-assert-equals = (term-let-assert-equal (assignment-list ...) term-template term-template)
assignment-list ::= (pattern-variable integer term-template)
```


While this form is based off `term-let` form provided by PltRedex, the way assignments are specified is different. In PltRedex, assignment is `(pattern term)` (i.e. term is matched against the pattern and terms bound by the match are then used to replace appropriate pattern-variables), whereas PyPltRedex bypasses matching step. 

`integer` in assignment represents ellipis depth of the pattern-variable and assumes that related term is well-formed with respect to ellipsis depth. That is, `(n 1 (term (1 2 3)))` is valid but `(n 1 (term ((1) (2) (3))))` is not.

Sample usage of this form can be seen below:

```
(term-let-assert-equal
  ([n_1 1 (term (1 2))]
   [n_2 1 (term (3 4 5))])
  (term ((n_1 ...  n_2 ...) (n_2 ... n_1 ...)))
  (term ((1 2 3 4 5) (3 4 5 1 2))))
```

####Codegeneration

Generated code needs to do the following:

1. Generate term for each pattern-variable assignment and store each assignment in fresh `Match` object.
2. Generate actual term `t` given previously created `Match` object.
3. Generate expected term given empty `Match` object.
4. Ensure both terms are equal i.e. have the same structure.

```
def genTermLetAssertEqual(actual_termtemplate, expected_termtemplate, assignments):
	actualproc = codegen(actual_termtemplate)  
	expectedproc = codegen(expected_termtemplate)
	procedures = []
	for patternvariable, termtemplate in assignments:
		procedures.append( codegen(termtemplate) )
	procedurename = beginprocedure()
	emit( match = Match() )
	for i, patternvariable, _ in enumerate(assignments):
            fb.AssignTo(tmp1).New('Match')
            fb.AssignTo(tmp2).FunctionCall(procedures[i], tmp1) 
            fb.AssignTo(tmp3).MethodCall(match, MatchMethodTable.AddKey, rpy.PyString(patternvariable))
            fb.AssignTo(tmp4).MethodCall(match, MatchMethodTable.AddToBinding, rpy.PyString(patternvariable), tmp2)
	fb.AssignTo(tmp0).FunctionCall(templatetermfunc, match)
	fb.Print(tmp0)
	fb.AssignTo(tmp1).FunctionCall('asserttermsequal', tmp0, expected)
	endprocedure()

	nameof_this_func = self.symgen.get('asserttermequal')
	self.modulebuilder.Function(nameof_this_func).Block(fb)
	self.modulebuilder.AssignTo(tmp1).FunctionCall(nameof_this_func)

```

# apply-reduction-relation-once-assert-equal
