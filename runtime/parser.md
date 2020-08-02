# Processing Input.
Initially, input to PltRedex is read from the file and stored as a string. To be able to apply reduction-relation, the string needs to be analyzed. There are two parts:

* Lexical analysis that breaks up the string into individual tokens and decides which kind of token it is.
* Parsing - given a set of tokens, produce valid terms.

## Lexical analysis

### Description

Most commonly tokens are described using regular expressions. Below is description of token kinds supported by PyPltRedex.
* Comments - `;.*\\n`  - matches semicolon followed by zero or more characters and ends with newline. Discared
* Opening parentheses - `\[\{\(`
* Closing parentheses - `\]\}\)`
* Strings - `\"([^\"\\]|(\\"))*\"`  - TODO
* Integers - `(\+|\-)?[0-9]+` Optional plus/minus + one or more digits. In most imperative programming languages minus sign would have been interpreted as an operation on the number. In Racket, minus sign is a part of a number - whitespace between minus sign and number is important (TODO expand)
* Decimal numbers: `(\+|\-)?[0-9]*\.[0-9]+`. Plus/minus signs are optional, followed by zero or more digits, followed by the dot and more than one digits. 
* Identifiers:  `([^ \(\)\[\]\{\}\"\'`;\#\n])*([^ \(\)\[\]\{\}\"\'`;\#0123456789\n])+([^ \(\)\[\]\{\}\"\'`;\#\n])*` Identifiers are not allowed to contain parentheses, quotes, pound signs and whitespace. To differentiate between identifier and number, identifier must contain at least one non-numerical character. Thus, regular expression has to contain three parts:  (1) Zero or more symbols matching anything but reserved symbols. (2) One or more symbols matching anything except reserved symbols and digits; (3) Zero or more symbols matching anything but reserved symbols.

### Implementation.

Actual lexer implementation doesn't use all regular expressions as described above but implements their functionality programmatically. The following procedures are defined to detect whitespace, newline and reserved symbols.

```
def is_whitespace(c):
    return c == ' ' or c == '\t' or c == '\n' or c == '\r'

def is_newline(c):
    return c == '\n'

def is_reserved(c): 
    return c in ['(', ')', '[', ']', '{', '}', '\"', '\'', '`', ';', '#', '|', '\\']
```


UML class diagram for Lexer can be seen below.

```
class Tokenizer:
	string : String
	start : int
	end : int
	advance() : void
	peek() : char
	extract_if_contains(substring: string) : string
	extract() : string
	next() : string
```

* `string` is the string that requires lexical analysis.
* `start` and `end` are indices indicating an interval within the `string`. The substring that ends with index `start` has already been analyzed. A substring between `start` and `end` is a potential token. Any substring after `end` requires analysis.
* `advance()` method increments `end` by one.
* `peek()` returns a character at index `end` of the `string`.
* `extract_if_contains(substring)` extracts substring `s` beginning at `start` and ending at `start+len(substring)` and compares it against provided `substring`. If both strings are equal, `start` and `end` indices are set to `start+len(substring)` and True is returned. Otherwise, False is returned.
* `extract()` extracts the string between `start` and `end`, sets `start=end` and returns the extracted string.
* `next()` returns the next token in the string. 

### Next method.
This method implements actual tokenization logic. The algorithm is as follows:

* `peek` the character `c`.
* If `is_whitespace(c)` is True then `advance` and `extract`. This will essentially ignores the characters altogether.
* If `c` is semicolon, `advance` and consume any character until newline. `advance` to consume newline. The result of `extract` is discarded. If `end-of-file` is encountered, stop trying to consume characters.
* if `c` is one of opening parentheses, return pair `(LParen, extract()`
* if `c` is one of closing parentheses, return pair `(RParen, extract()`
* If `c` is double-quote, `advance`. Consume characters until matching double-quote is encountered. If during consumption backward slash is encountered, character that immediately follows must also be consumed (i.e. it is escaped character). If `end-of-string` character is encountered, raise exception as the string doesn't terminate. Return `(String, extract())`
* If `c` is pound symbol `#`, call `extract_if_contains` twice with following arguments: `#t`, `#true` and `#f`, `#false`. Upon success return `(Boolean, #t)` or `(Boolean, #f)`. Otherwise, raise Exception.
* Otherwise, a token must be either an integer, decimal or identifier. To identify these regular expressions are used, but first they have to be extracted. Consume all characters `c` such that they are not `is_whitespace(c)`, `is_reserved(c)` or `end-of-string`. Let `s=extract()`. 
	* If `match(IntegerRegex, s)` return (Integer, s)
	* If `match(DecimalRegex, s)` return (Float, s)
	* If `match(IdentRegex  , s)` return (Ident, s)
	* Otherwise, raise Exception - token kind is unknown
* Goto step 1 until `c` is `end-of-string`.

## Parsing

Terms have the following grammar:

```
term = term-sequence atom
term-sequence = (term ...) 
atom = integer 
	 | string
	 | (-|+)?[0-9]+\.[0-9]+
	 | #t
	 | #f
	 | identifier
```


### Implementation

TODO umldiagram?



