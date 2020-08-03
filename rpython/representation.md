## Compile-Time Representation

PyPltRedex works with **abstract syntax trees** (AST) and then emits RPython source code by traversing the tree and emitting strings. Abstract syntax tree itself is a tree that represent constructs of the language such as arithmetic operations, assignments, loops, etc.

In Python and other imperative languages, nodes of an abstract syntax tree can be split into two categories:

* Statements such as loops, if/else statements, variable assignments.
* Expressions such as arithmetic operations, array element access, literal values such as integers or strings, etc.

However, creating trees can be quite annoying due to its recurive nature - to express expression `a =1 + 2 + 3` several nodes have to be created - `Assign(a, Add( Add( Integer(1), Integer(2)), Integer(3)))`. 

PyPltRedex's AST definition is modified to include `PyValue` - subset of Expressions that includes only variables and literals. Remaining expressions are now required to use `PyValue`. This way, expression like `a = 1 + 2 + 3` cannot be expressed and one would have to introduce extra variables to express such statements - `b = 1 + 2; a = b + 3`. This makes it similar to typical three-address code intermediate representation that most compilers employ.

UML diagram for statements, expressions and values can be seen below.



## Rpython Abstract Syntax Tree Creation.

Manually creating AST can be tedious. PyPltRedex provides fluent interface for creation of AST nodes - `BlockBuilder`. The goal of the block-builder is to construct code blocks which may, for example, be a body of a function or body of the loop. 

State diagram for the `BlockBuilder` can be seen below:

Circled states are finite states that actually create AST nodes and append them to the block. Rectangled states are class definitions. Edges annotated with `instantiate` indicate intermediate object creation; for example, calling `For` creates new `ForPhase1` object and initializes it with `*args`. 

The code snippet below shows (a) piece of code being compiled; (b) direct AST construction; (c) using fluent interface.
```
(a)
a = 0
for i in array:
	a = a + i

a, i, array = PyId('a'), PyId('i'), PyId('array')

# without any interfaces
#(b)
Assign(a, PyInt(0))
forb = [ Assign(a, BinaryExpr('+', a, i)) ]
ForStmt(i, array, forb)

# with fluent interface.
#(c)
forb = BlockBuilder()
forb.AssignTo(a).Add(a, i)

bb = BlockBuilder()
bb.AssignTo(a).PyInt(0)
bb.For(i).In(array).Block(forb)
```

## Potential Improvements.

As one may have noticed, `BlockBuilder` doesn't handle variable creation. Initially it was not such a problem as most of the generated functions are quite small but it becomes more confusing when functions are decently sized. Code snippet from above could be rewritten in the following manner:

```
forb = BlockBuilder()
a = forb.AssignTo().Add(a, i)

bb = BlockBuilder()
a = bb.AssignTo().PyInt(0)
i = bb.Declare('i')
bb.For(i).In(array).Block(forb)
```


