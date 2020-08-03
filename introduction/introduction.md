# Introduction

## Motivation

PltRedex is domain-specific language embedded into Racket designed for specifying and debugging operational semantics. By specifying a language and reduction rules, PltRedex is able to apply reduction rules to terms by rewriting them. (FIXME) PltRedex also provides randomized testing functionality.

However, after testing PltRedex specification one might want to turn it into stand-alone interpreter and that's when dependency on Racket turns into a problem for the following reasons:

1. One have to ship entire Racket runtime to be able to run the specification.
2. Racket is not particularly fast. 

PyPltRedex is the tool that attempts to solve the problem by taking PltRedex specification and compiling it into RPython language - statically analyzable subset of Python programming language that is used for implementation of interpreters within the PyPy toolchain. Using RPython toolchain, resulting RPython program is then compiled into stand-alone, more efficient and considerably more low-level version of the program. However, by removing Racket from the equation, the specification has to be modified to use RPython instead.

## Goals 

Since PltRedex has existed for a while and provides wide range of functionality ranging from language specification, type checking and testing, PyPltRedex implements tiny subset of PltRedex that is enough to be usable. In particular,

* Only a subset of pattern language provided by PltRedex is supported.
* Only functionality required for term rewriting is supported.

## Thesis Outline
TODO
