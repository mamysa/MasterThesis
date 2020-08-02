## Ellipsis Depth Example.

Given pattern `((number ...) ...)` and term `((1 2 3)())`, the matching algorithm should return `Match` instance with `number = ((1 2 3)())`, i.e. the pattern matches the term exactly. The diagram below shows how using `increasedepth` and `decreasedepth` methods provided by `Match` facilitate the matching. Note, however, that the example doesn't show the copying aspect of matching and assumes that matches are copied behind the scene. 

* (a) shows the state before the matching begins. Recall that `Match` uses `Binding` objects that internally use a stack to store terms. Initially the stack is empty.
* (b) First element of the sequence is being processed. Since it is ellipsis, (1) `increasedepth` is called this pushing an empty sequence onto the stack and (2) calls matching procedure for pattern `(n ...)` with term `(1 2 3)`.
* (c) First element of the pattern `(n ...)` is being processed. (1) `increasedepth` is called this pushing an empty sequence onto the stack and (2) calls matching procedure for pattern `n` with term `1`. 
* (d) Since `1`  matches `number`, `addtobinding` method is called with term `1`. This appends `1` to the topmost sequence on the stack.
* (e) Shows repeated call of matching procedure for pattern `n` with terms `2` and `3`. Each one of them is processed exactly in the same way as term `1` in (d) - `2` and `3` are appended to the topmost sequence on the stack. 
* (f) Since there's no more numbers to match, matching of pattern `n ...` is now complete and for each match aquired so far `decreasedepth` is called. This action takes topmost element on the stack and appends to the previous sequence on the stack. 

We have to complete matching of pattern `(n ...)`. At this point there are several matches with following assignments:  

```
n =         0 3
n = ((1))   1 3
n = ((1 2)) 2 3
n = ((1 2 3)) 3 3
```

The only valid match is the one containing ((1 2 3)) because others fail to consume all terms in the sequence and thus discarded.

* (g) The second and last element of the outer term sequence is being processed - `()`. Increase. Begin matching term `()` against pattern `(n ...)`.

* (h) The first element of the pattern `(n ...)` is being processed. Since it is `n ...`, call `increasedepth` thus pushing empty term sequence onto the stack. 

* (i) However, since term `()` doesn't contain any numbers and matching procedure for pattern `n` cannot be called, `decreasedepth` is called thus appending empty term sequence to the previous sequence on the stack. 

* (j) Since there are no more terms to be matched by outer ellipsis, `decreasedepth` is called. However, since stack contains only a single term sequence, no action is performed. This completes matching pattern `(n ...) ...`. 

Need to complete matching of pattern `((n ...) ...)`. There are three matches:

```
Match(n=), 0, 2
Match(n=((1 2 3)) 1 2
Match(n=((1 2 3) ()) 2 2
```

There's only a single match with `n=((1 2 3) ())` that was able to consume all the terms in the sequence. This is the final result.

Since the stack is only manipulated by `increasedepth` and `decreasedepth` methods which are only while matching patterns under ellipsis, it can be seen that, for example, term `((((1 2 3))) ((())))` will produce exactly the same match as for term `((1 2 3) ())`.

