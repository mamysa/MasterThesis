# UnresolvedSymbol Resolution Pass

Immediately after parsing Redex specification, it is unknown whether certain elements of pattern are built-in patterns or non-terminal symbols or just literals. These elements will be represented with `UnresolvedSymbol(symbol)` instances. Given `define-language` structure, or more specifically a list of non-terminals defined by the language, by analyzing the `symbol` it is possible to decide if given symbol should be a non-terminal or built-in pattern. 

The symbol is analyzed in the following way: locate first underscore character. If there are no underscore characters, simply return the symbol, otherwise return all characters before the underscore. If underscore is the first character of the symbol, raise an `Exception` because Redex doesn't consider such symbols valid. Resulting symbol will be refered to as *prefix*.

Resolution algorithm proceeds in the following manner. The pattern is traversed recurisely. When coming across `UnresolvedSymbol(symbol)` node, extract prefix from the symbol. One of the following things may happen:

* Prefix is *number*, replace unresolved symbol with `BuiltInPattern(Number, symbol)`
* Prefix is *integer*, replace unresolved symbol with `BuiltInPattern(Integer, symbol)`
* Prefix is *real*, replace unresolved symbol with `BuiltInPattern(Real, symbol)`
* Prefix is *natural*, replace unresolved symbol with `BuiltInPattern(Natural, symbol)`
* Prefix is *string*, replace unresolved symbol with `BuiltInPattern(String, symbol)`
* Prefix is *boolean*, replace unresolved symbol with `BuiltInPattern(Boolean, symbol)`
* Prefix is *variable-not-otherwise-mentioned*, replace unresolved symbol with `BuiltInPattern(VariableNotOtherwiseMentioned, symbol)`
* Prefix is *hole*, replace unresolved symbol with `BuiltInPattern(Hole, symbol)`
* Prefix is found in the list of non-terminal symbols defined by the language, replace unresolved symbol with `Nt(symbol)`.
* Finally, check that symbol contains no underscores. Redex only allows underscores after non-terminal symbols and built-in patterns. Abort compilation if that is the case. Otherwise, replace unresolved symbol with `Lit(Variable, symbol)` and and the symbol to the set of literal variables defined in the language.
