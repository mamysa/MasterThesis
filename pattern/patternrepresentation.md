# Pattern 

This section describes subset of PltRedex's pattern specification language supported by `PyPltRedex`. Grammar for the pattern language can be seen below, in EBNF notation. 

```
pattern = number 
        | integer 
		| real 
		| natural 
		| string 
		| boolean 
		| variable-not-otherwise-mentioned 
		| hole 
		| symbol
        | (in-hole pattern pattern)
        | (pattern-sequence *) 
pattern-sequence : pattern 
                 | pattern ...  # literal ellipsis
```

* *number* pattern matches any number.
* *integer* matches any exact integer. 
* *real* matches any real number.
* *natural* matches any natural number; that is any non-negative integer.
* *string* matches any string.
* *boolean* matches any boolean - `#t` or `#f`.
* *variable-not-otherwise-mentioned* matches any symbol that is not used as a literal in language definition. For example, if language definition contains pattern `(+ number number)` `variable-not-otherwise-mentioned` will not match symbol `+`.
* *hole* matches `hole` term exactly.
* *symbol* matches any symbol except if its value coincides with non-terminal symbol in language definition.

All pattern above except *hole* can be suffixed with underscore and identifier (for example, number_1`) to create binding to matched term.

*(in-hole pattern pattern) traverses the term trying to match the second pattern; upon successful match the term matching the second pattern is replaced with term `hole` and then the first pattern is matched. First pattern must match exactly one hole.

*pattern-sequence* pattern matches a term list, where each pattern-sequence element matches an element of the list. Each individual pattern within the sequence can be suffixed with `...` (literal ellipsis) and that will match zero or more terms matching the pattern.

If patterns in the pattern-sequence are suffixed with the same identifier (e.g. `(number_1 number_1)`)), then the match is contrained to terms that are equal. That means term `(1 1)` matches the pattern but `(1 2)` does not. For patterns in `define-language` constraint checking is not performed. PltRedex provides other constraint checks but they will not be considered.

# Compile-time representation of patterns.

Pattern language described above maps to following classes: 

* `BuiltInPattern(TAG, ident)` represents `number`, `real`, `integer`, `natural`, `string`, `boolean`, `variable-not-otherwise-mentioned` and `hole` patterns. It must be appropriately tagged to distinguish between patterns. For example, pattern `number_1` is represented as `BuiltInPattern(Number, number_1)`.
* `Nt(ident)` represents non-terminal symbols.
* `Lit(TAG, symbol)` represents any literal symbol encountered in the pattern. These can be integers, decimal numbers, strings, boolean, etc and are matched exactly. Tag must be provided to distinguish between literal kinds. For example, pattern `my-var` is represented as `Lit(Variable, my-var)`
* `UnresolvedSym(ident)` represents a pattern that can be transformed either into non-terminal or literal symbol after analyzing related language definition.
* `Repeat(pattern)` represents a pattern under ellipsis.
* `PatSequence(pattern ...)` represents pattern sequences with arbitrary number of patterns. 
* `InHole(pattern, pattern)` represents `in-hole` patterns.

# Pattern Analysis Passes
This section describes analysis / transformation passes needed before being able to generate code for patterns. More specifically, this is a list of required transformations:

* Non-terminal resolution.
* Make bound identifiers unique. 
* Checking ellipsis depth of identifiers.
* Non-terminal cycle checking.  
* Non-terminal graph construction and `hole` reachability.
* `in-hole` pattern `hole` checker. 
* Constraint check insertion.
* Assignable identifier extraction.




