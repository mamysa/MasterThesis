#Introduction
	- PltRedex
	- Goals - use PyPy RPython to make thing faster.
	- Thesis outline.

# Features of PLtREdex
- Theory: term rewriting systems
- PltRedex overwiew.
- Theory: evaluation contexts.

# RPython
- What is it?
- Compile-time representation.
- AstCreation 

# Runtime 
- Runtime representation of Terms.
- Runtime representation of matches.
- Fresh and arithmetic utils.
- Parsing terms

Alternate outline - add extra chapter
# Compile-Time Representation of PltRedex
- Top-level forms
- Patterns
- Terms


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
	              - better error reporting
				  - merging patterns?
				  - define-judgment-form
