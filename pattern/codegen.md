# Pattern Code Generation
Since patterns contain built-in subpatterns such as numbers and non-terminal symbols defined by the language, there has to be a way to decide if given subterm matches subpattern.

Pattern matching requires three kinds of procedures.

* `isa` procedure that accepts a term and decides (true/false) if it matches desired pattern. Such functions are generated for most built-in patterns such as numbers or strings and for each non-terminal symbol in the language. These do not consume terms by themselves.
* Actual matching procedure that accepts a match object, a term, and two extra arguments `head` and `tail` which indicate a range of subterms in the term that haven't been matched yet. Successful matching changes values of `head` and `tail` by increasing and decreasing them, respectively. This kind of procedure returns a list of of `match`,`head`,`tail` triples. 
* Top-level matching procedure that accepts a term, initializes `Match` object with assignable symbols in the pattern and calls matching procedure, after which `Match` objects filtered and returned.

## Matching procedures.

It is assumed that all `isa` procedures have been already generated and their names are known.

Match procedures have the following interface:

`def matchfunc(match: Match, term: Term, head: int, tail: int) -> [ (Match, int, int) ]

### Matching Built-in patterns and Non-Terminal.
Most built-in patterns such as numbers, integers or strings as well as non-terminals are matched in the same way by calling appropriate `isa` procedure. Upon successful match, term is assigned to appropriate variable in `Match` object, `head` argument is incremented and list containing `match`, `head`, `tail` triple is returned. In case if `hole` built-in pattern is being matched then matched term is not assigned and `match` object remains unmodified. 

In the code snippet below `isafunction` is a stand-in for actual `isa` procedure to be called.

```py
tmp0 = isafunction(term)
if tmp0 == True:
  tmp1 = match.addtobinding(sym, term) 
  head = head + 1
  return [(match, head, tail)]
return []
```

### Matching Literals
As a reminder, a term is tagged with its kind. Matching a literal symbol in the term involves kind comparison (i.e. ensuring the term is indeed an integer or string, for example) and then comparing if value of the term is indeed the one expected. `head` is then incremented and list containing `match`, `head`, `tail` triple is returned. Code in figure below matches term `7`.

```py
tmp0 = term.kind()
if tmp0 == TermKind.Integer:
  tmp1 = term.value()
  if tmp1 == 7:
    head = head + 1
    return [ (match, head, tail) ] 
return [] 
```

### Matching patterns under ellipsis.

Recall that patterns under ellipsis match lists of terms and can only be contained in pattern sequences. Non-deterministic matching repetition of terms is handled in the following way.

* For each symbol to be assigned in subpattern, call `increasedepth` method of `match` object. This will push an empty term sequence onto the stack. (see Match object design in Chapter ??)
* Create a list of matches to be returned later. It is initialized with initial `match`, `head`, `tail` procedure arguments.
* Initialize a queue of matches with same initial `match`, `head`, `tail` arguments. The reason why queue is needed to store usual `(match, head, tail)` tuples because patterns under ellipsis may also contain non-deterministic ellipses and hence to obtain all desired matches a matching procedure under ellipsis also needs to be called on such matches.
* While queue is full 
	* Remove `(match, head, tail)` from the queue. If `head` and `tail` are equal then it means all elements of the term have been matched and there's nothing left to do.  Otherwise, create a copy of `match` object (which will also copy terms stored in `match`)
	* Retrieve an element of the term sequence and call matching procedure for pattern under ellipsis. Add newly obtained matches both to `matches` and queue.
* For each obtained `match` object call `decreasedepth` method. This completes matching the list of terms.
* `matches` contains all desired matches.

Code snippet below shows the implementation of the procedure for some pattern, for example `(n_1 ...)`. Aside from increasing / decreasing ellipsis depth (different patterns require different assignable symbol), such ellipsis matching logic is used for every ellipsis pattern.

```py
tmp0 = match.increasedepth('n_1')
tmp1 = (match, head, tail)
matches = [ tmp1 ]
queue   = [ tmp1 ]
while len(queue) != 0:
  m, h, t = queue.pop(0)
  if h == t:
     continue
  m = m.copy()
  tmp2 = term.get[h]
  tmp3 = match_term(tmp2, m, h, t)
  matches = matches + tmp3
  queue   = queue + tmp3
for m, h, t in matches:
  tmp4 = m.decreasedepth('n_1')
return matches
```

### Matching sequences.

Matching pattern sequences is more involved. This assumes that subpatterns have been generated already and names of procedures are known. 

* First, given term must be a sequence. If it is not, an empty list is returned.
* Then, the term has to be "entered" to be ready for matching; that is, to be able to use subpattern procedures to match subterms new values for `head` and `tail` are required. Initialize `nhead=0` and set `ntail` to be length of the term sequence - these will be used to track which elements of the term haven't been matched yet.
* Before matching elements of the term, need to ensure that number of said elements is greater or equal to the number of elements in the pattern sequence excluding patterns under ellipses and constraint checking nodes. Terms with too few elements do not match the pattern. For example, term `(3)` does not match pattern `(n_1 n_2 ... n_3)` as `n_1` and `n_3` have to be matched exactly.
* Create an empty list of matches and initialize it with `(match, ntail, nhead)` pattern.
* Now, we can start matching individual elements of the term according to the elements of the pattern sequence. There are few cases to consider here. Ellipses and constraint checks have to be handled separately from everything else.  Ellipses are handled in their own procedure and it must be provided the entire term; constraint checks do not actually match anything.

* For each tuple `(m, h, t)` in the list of matches:
* If given element `e` with offset `i` in pattern sequence is Ellipses (Repetition), simply call repetition procedure with arguments `(m, term, h, t)`. For each of obtained matches, we need to ensure number of unmatched elements in the term is greater or equal to number of non-optional patterns between `i` and length of the sequence. Matches not satisfying requirement above are discarded. If the list of matches after filtering is empty, given term does not match the pattern at all. Code snippet below demonstrates matching patterns under ellipses in pattern sequences.

```py
matches1 = []
for m,h,t in matches:
  tmpi = match_repetition_of_n(term, m, h, t)   
  matches1 = matches1 + tmpi
num_required = sequence.get_number_of_nonoptional_matches_between(i, len(sequence))
matches2 = []
for m, h, t in matches1:
  tmpi = t - h
  if tmpi >= num_required:
    tmpj = matches2.append((m, h, t))
if len(matches2) == 0:
  return matches2 
```

If given element `e` is `CheckConstraint` with symbols `x` and `y`, then ensure that `match[x] == match[y]`. If none of the matches pass the test, return an empty list.

```py
matches{i} = []
for m, h, t in matches{i-1}:
  tmp{i} = m.CompareKeys(sym1, sym2)
  if tmp{i} == True:
    tmp{j} = matches{i}.append( (m, h, t) )
if len(matches{i}) == 0:
  return matches{i} 
```


* For everything else, call matching function.

```py
matches{i} = []
for m, h, t in matches{i-1}:
  tmp{j} = term.get(h)
  tmp{i} = func(tmp{j}, m, h, t)
  matches{i} = matches{i} + tmp{i}
if len(matches{i}) == 0: 
  return  matches{i} 
```


TODO exit term



## Matching in-hole
In-hole pattern consists of two patterns. The term is traversed recursively trying to find a subterm that matches the second pattern. If such subterm is found, the term is copied from previously mentioned subterm all the way to the root and subterm is replaced with term `hole`. Copying is needed because original term must be left intact.

For recursive term traversal a path from root of the term to possible subterm matching the second pattern is maintained. This allows for only copying terms/subterms that will be affected by `hole` substitution instead of copying the entire term.

Due to possible non-determinism, `match` object must remain unmodified. For both patterns of `in-hole`, separate `Match` objects are created and initialized with appropriate meta-variables. Upon successful matching by both procedures, Cartesian product between matches of both lists is computed and results are inserted into a copy of initial `match` object. By construction, all meta-variables of `Match` objects are unique.

```py
def inhole(term, match, head, tail, path):
	matches = []
	inpat2match = Match(...)
	pat2matches = pat2matchfunc(term, inpat2match, 0, 1)
	if len(pat2matches) != 0:
		inpat1match = Match(...)
		tmp0 = path + [term]
		tmp1 = copy_path_and_replace_last(tmp0, hole)
		pat1matches = pat1matchfunc(tmp1, inpat1match, 0, 1)
		if len(pat1matches) != 0:
			tmp11 = head + 1
			for m1, h1, t1 in pat1matches:
				for m2, h2, t2 in pat2matches:
					tmp2 = combine_matches(m1, m2)
					tmp{i} = match.copy()
					tmp{j} = tmp2.getbinding(...)              ; same for inpat2match
					tmp{k} = tmp{i}.addtobinding(..., tmp{j})  ; same for inpat2match
					tmp3 = matches.append((tmp{i}, tmp11, tail))
	tmp4 = term.kind()
	if tmp4 == Term.Sequence:
		tmp5 = path.append(term)
		tmp6 = term.length()
		for tmp10 in range(tmp6):
			tmp7 = term.get(tmp10)
			tmp8 = inhole(tmp7, match, head, tail, path)
			matches = matches + tmp8
		tmp9 = path.pop()
	return matches 
```

From Figure ?? above it can be seen that procedures matching `in-hole` patterns require an extra parameter `path`.  Thus, to conform to desired interface, additional wrapper procedure is created to call actual `in-hole` procedure with `path` being an empty list. 

This is not all, however. Since `in-hole` patterns may also require constraint-checking, doing that in such wrapper function is good (TODO REPHRASE ME)

(TODO add code snippet)
(redex-match A (in-hole ((n ...) hole (n_2 ...)) (n_2 ...))  (term ((1 2 3) (5 6 7) (5 6 7))))

## Top-level pattern matching procedures.

Top-level pattern matching procedures have the following interface:

`def matchfunc(match: Match) -> [Match]`

This procedure creates `Match` object, initializes it with assignable symbols seen in the actual pattern and calls appropriate matching procedure. `head` and `tail` parameters are set to zero and one, respectively. Since matching procedure returns a list of `(match, head ,tail)` tuples, `Match` objects are filtered out and returned.

For example ... 

## Is-A procedure.

So called Is-A procedures have the following interface `isa(term: Term) -> boolean`. These procedures are generated for all built-in patterns excluding `(inhole pattern pattern)` as well as non-terminal symbols defined in `define-language` form.

### Built-in patterns

For most built-in patterns isa-procedures are generated in a way similar to matching literal terms, as explained above - by comparing the tag of a term against desired tags.  For example, for `number` pattern term can be tagged with either `Integer` or `Float`.

```py
tmp0 = term.kind()
if tmp0 in [TermKind.Integer, TermKind.Float]:
  return True
return False
```

The only built-in pattern that has to be handled slighly differently is `variable-not-otherwise-mentioned` which also checks if value of a term tagged with `Variable` is not in the set of reserved symbols obtained during non-terminal resolution. Figure below demonstrates this.

```py 
tmp0 = term.kind()
if tmp0 == TermKind.Variable:
  tmp1 = term.value()
  if tmp1 not in ['+', '-']:
    return True
return False
```



## End
This completes code generation for patterns.
