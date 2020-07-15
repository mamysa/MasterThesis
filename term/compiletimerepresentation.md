Compile-time representation of terms is very different from runtime representation described previously. The reason for that is the necessity to handle ellipses; or, more specifically substitution of pattern variables under ellipses - `PltRedex` handles this dynamically and erroneous ellipses aren't detected until term creation time.
(FIXME is this factual?)
We want to handle ellipsis depth checking of pattern variables at compile time to be able to provide compile time error messages. Doing this allows for complete elimination of ellipses from the runtime (with variable `...` being a reserved symbol that throws an exception). In addition, this also allows for detection of metafunction applications statically.


## Compile-time representation.

* `TermLiteral(kind, value)` represents runtime term and is compiled into runtime representation directly.
* `PatternVariable(sym)` represents a symbol that must be replaced with some term from given `Match` object.
* `UnresolvedSymbol(sym)` represents a symbol that could either be `TermLiteral` or `PatternVariable`; this is decided by assigned variables stored in `Match` object. 
* `Repeat(term-template)` represents term-template under ellipsis. Since our goal is to resolve all ellipsis at compile-time, the term-template under ellipsis must contain at least one pattern variable for `Repeat` to be well-formed.
* `TermSequence(term-template ...)` is a sequence of term-templates. These will become actual runtime term sequences.
* `InHole(term-template1, term-template2)` term-template is dual to `InHole` pattern that constructs new term given two terms.
* `PythonCall` represents Python function calls.
* `MetafunctionApplication` represents metafunction applications. Their detection will be explained later.


From now on compile-time terms will be referred to as *term-templates* while runtime terms will be simply refered to as *terms*. *Child term-template* refers to any term-template contained in `TermSequence`, `Repeat` and `MetafuntionApplication`.

## Term-Template Ellipsis Depth Checking Pass

As mentioned before, our goal is to resolve all ellipses at compile time by ensuring that there are no patterns under ellipses that do not have at least a single pattern variable. In addition, unresolved symbols must be resolved based on variables assigned in `Match` object. 

At this stage, since pattern variables will need to be replaced with terms, inputs to term-templates are detected. This is done by annotating term-templates. The following annotations are introduced:

* `InArg(parameter_name)` - some pattern variable term-template or any of its child term-templates is replaced with term (or subterm) assigned to `parameter_name`. 
* `ReadMatch(parameter_name, sym)` takes a term from `Match[sym]` and assigns in to `parameter_name`. If there happens to be some child term-template containing pattern variable with value `sym`, this means that all term-templates on the path to that specific child term-template will be annotated with `InArg(parameter-name)`.
* `ForEach(parameter_name)` annotation is added to `Repeat(term-template)` term-templates and means that every element of the term sequence assigned to `parameter_name` must be plugged in child term-template assuming the term has compatible ellipsis depth.

Explanation of `parameter_name` is needed. These are used to prevent name collisions ... (TODO exammple)

Below follows the description of the algorithm.

To perform annotation, a path of term-templates must be maintained to be able to count all ellipsis on the path to the root term-template. A structure of `Match` object (i.e. a list of variables and ellipsis depth of matched terms) is also known (from chapter???). Given all, start recursive term-traversal.

When any term-template is visited, it is added to the top of the path stack. When term-template and its child term-templates have been visited, top-most element is popped from the stack. Now we consider term-templates that may be visited.

* UnresolvedSymbol




