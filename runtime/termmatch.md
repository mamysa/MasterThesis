
## Runtime representation of Term

Terms are represented in the following way. (uml diagram?) As one may notice, these classes are all very similar but due to RPython's type inference an attempt to merge them results in compile-time error:

```
class LeafNode:
    def __init__(self, kind, value):
        self.kind = kind 
        self.value = value

def entrypoint():
    p = LeafNode(1, 'hello world!')
    q = LeafNode(2, 12.5)

# UnionError:
#  SomeString(const='hello world!', no_nul=True)
#  SomeFloat(const=12.5)
```

Since the `LeafNode` instance is created with `hello_world!` string, any other instantiation of LeafNode expects it's second argument to be of type `string`. 

TODO explain methods.
`shallow_copy`
`deep_copy` 
`equals`
`tostring`

### Helper procedures.
`copy_path_and_replace_last`

## Runtime representation of Matches


`Binding` class encapsulates a stack of terms and provides three methods for its manipulation:

* `increase_depth` pushes term `Sequence` onto the stack provided a term on top of the stack is also a `Sequence`, otherwise raises an error.
* `decrease_depth` has the following behaviour:
        1. if stack is empty, raise exception
        2. if stack size is 1 and topmost element is not term `Sequence` raise exception.
        3. if stack size is 1 and topmost element is term `Sequence` do nothing.
        4. if stack size > 1, pop topmost element and append it to element below. ( works because increasedepth must be called beforehand)
* `add(term)` has the following behaviour:
        1. if stack is empty, add value
        2. if stack is not empty and not a compoundarray, raise exception
        3. if stack is not empty and is compoundarray, add value to the array.

Usage of these methods will be described later in chapter Pattern.

`Match` class stores a dictionary of strings to `Binding` instances and represent pattern-variable assignments. 

* `increase_depth` calls `inrease_dpeth` method of relevant `Binding` instance.
* `decrease_depth` calls `decrease_depth` method of relevant `Binding` instance.
* `addtobinding` calls `add` method of relevant `Binding` instance with `term`.

* `comparekeys(key1, key2)` compares topmost terms on stacks of bindings assigned to key1 and key2.

* `deepcopy` creates a new Match instance with all `Binding` and `Term` instances contained within copied recursively.
