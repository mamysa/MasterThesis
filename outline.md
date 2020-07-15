# Introduction
	- PltRedex
	- Goals - use PyPy RPython to make thing faster.

# Features of PLtREdex
	- Define-lagnuage
	- redex-match
	- redex-let
	- define-reduction-relation
	- define-metafunction
	- apply-reduction-relation

# PyPy rpython

# Common 
- Runtime representation of Terms.
- Runtime representation of matches.

# Pattern Matching
	- Basic features of pattern matching.
		- Pattern grammar.
		- Pattern sequences
		- Repetitions.
			- non determinism in repetitions.
		- Constraint checking.
	- Preprocessing pattern in any context
		- Non-terminal resolution
		- Ellipsis match mode.
		- Assignable Symbol extraction
	- Preprocessing define language
		- Uniquify Identifiers 
		- NtCycleChecking  ( this is wrong)
		- HoleReachability.
	- Preprocessing patterns in define-reduction-relation/metafunction/etc
	-Code generation
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
	- define-reduction-relation
		- Features
		- Codegen
	- define-metafunction 
		- Features
		- Codegen

# Testing/Evaluation
	- Testing forms (assert-equals etc)
	- Unittesting.


# Evaluation


