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
- Patterns
- Terms
- Top-level forms

# Analysis/Transformation Passes
- Pattern Preprocessing Passes
	- Non-terminal resolution
	- Uniquify Identifiers 
	- NtCycleChecking 
	- HoleReachability.
	- InHole checker
	- Constraint Check Insertion
	- Assignable Symbol Extraction
- Term Preprocessing Passes
	- Detecting inputs
	- Mf-apply
-Tlfrom preprocessing passes
	- definelang
	- metafunctions
	- apply-red
	- testing forms.

# Code Generation
* Patterns: 
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
* Terms:
	- Code generation
* Other forms:
	-Codegen

# Testing/Evaluation
	- Testing 
		- Unit Testing
		- Integration Testing.
	- Correctness?

# Conclusion
	- Future work - non-determinism detection and non-deterministic to deterministic ellipsis promotion.
	              - better error reporting
				  - merging patterns?
				  - define-judgment-form
