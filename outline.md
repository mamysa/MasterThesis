#Introduction
	- PltRedex
	- Goals - use PyPy RPython to make thing faster.

# Features of PLtREdex
	- Pattern Language
	- Term    Language
	- Define-lagnuage
	- redex-match
	- redex-let
	- define-reduction-relation
	- define-metafunction
	- apply-reduction-relation

# Rpython Runtime 
- Runtime representation of Terms.
- Runtime representation of matches.
- Parsing terms

# Pattern Matching
	- Pattern compile time representation.
	- Pattern Preprocessing Passes
		- Non-terminal resolution
		- Uniquify Identifiers 
		- NtCycleChecking 
		- HoleReachability.
		- InHole checker
		- Constraint Check Insertion
		- Assignable Symbol Extraction
	- Code generation
		- Basic overview - match functions, isa functions.
		- Matching functions
			- Matching numbers/variables/etc.	
			- Matching Literals.
			- Matching repetitions.
				- deterministic / non-deterministic
			- Matching pattern sequences.
			- Matching in-hole
		- TopLevel matching functions
		- IsaMatching functions

# Term generation.
	- Compile time representation.
	- Detecting inputs
	- Code generation

# Other forms
	- define-language
		- Compile-time-representation
		- Code generation for isa_functions for non-terminals
	- define-reduction-relation
		- Compile-time-representation
		- Preprocessing reductioncase
		- Preprocessing domain.
		- Codegen
	- define-metafunction 
		- Compile-time-representation
		- Handling contract.
		- Codegen

# Testing/Evaluation
	- Testing forms (assert-equals etc)
	- Unittesting.
	- Correctness?

# Conclusion
	- Future work - non-determinism detection and non-deterministic to deterministic ellipsis promotion.

