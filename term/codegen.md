# Term Code generation

## Input Generation
Recall that `Term_EllipsisDepthChecker` annotates term template with three kinds of annotations:
* `InArg(param_name)` is used to generate a signature of term-building procedure; value of `param_name` is included as parameter to the procedure. `match` parameter is implicit. 
* `ReadMatch(param_name, match_sym) indicates that there's a sequence of child term-building procedures that require a term assigned to `match_sym` in `Match` object. `match_sym` is passed to child term-building procedures if they contain annotation `InArg(param_name)`.

## Literal Terms.
Since literal terms turn into global variables and are compiled into runtime representation of terms, term-building procedure simply returns said global variable. For example, for some numerical term `5` such procedure is shown in figure below. 

```
lit0 = Integer(5)
def term_gen_lit0(match):
	return lit0
```

## Pattern Variables.
Term-template node that substitutes defined symbol with some term. Depending on presence of `InArg` or `ReadMatch` annotations, slightly different code may be generated. It is shown in figure below.

```
def term_termplate_gen1(match, x):
	return x

def term_termplate_gen2(match):
	x  = match.getbinding('x')
	return x
```


## TermSequence generation.

* First, for each `ReadMatch` annotation, produce assignment as described above. Now, we need to call term-building procedures of each element in the term-sequence-template. There are a few cases to consider here. 

* Element is `Repeat` (or ellipsis). To demostrate it, code that is generated for pattern `((x n) ...)` can be seen in the figure below. 
```
def gen_term('(x n) ...)', match):
	seq = TermSequence()
	x = match.getbinding('x')
	n = match.getbinding('n')
	num_elements = assert_list_sizes_match(x, n)
	for i in range(num_elements):
		xc, nc = x[i], n[i]
		nterm = gen_term('(x n)', match, xc, nc)
		seq.append(nterm)
	return seq

# InArg('x'), InArg('n')
def gen_term('(x n)', match, x, n):
  ...
```
First, note that our TermSequence-template has two annotation `ReadMatch('x', 'x')` and `ReadMatch('n', 'n')`. These assignments are generated in the obvious way on lines 3-4. Furthermore, since `Repeat` contain `ForEach('x')` and `ForEach('n')` annotations, it implies that both `x` and `n` are lists containing terms. Thus, child term-template of `Repeat` (that is, `gen_term('(x n)')`)  has to be called for each element in `x` and `n`. This implies that both lists have to be equal in size. `assert_list_sizes_match` procedure take any number of terms as an input and ensures their lengths are equal, otherwise it throws an exception. 


* Element is `PyCall`. Two insertion modes

* Otherwise, for any other term template kind its related term-building procedure is simply called with appropriate inputs.


## Python Calls
First, term-building procedures are generated for each term-template. Then, these procedures are called with appropriate arguments (which in this case is only `match` due to the way ellipsis are handled), and required Python function is called. Figure below shows generated code for term-template `,(addnums (term n_1) (term n_2))`.

```
gen_term(',(add(term n_1) (term n_2))', match):
	n_1 = gen_term('n_1', match)
	n_2 = gen_term('n_2', match)
	return add(n_1, n_2)

```

## In-Hole
Generate procedures for both term-templates. After calling them with appropriate arguments, `plughole` function is called. It locates `hole` in the first term and replaces it with the second term and returns resulting term.
