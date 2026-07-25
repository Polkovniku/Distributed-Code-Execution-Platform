const KEYWORDS = {
  python: [
    "print", "len", "range", "input", "int", "str", "float", "list", "dict",
    "set", "tuple", "bool", "type", "sum", "min", "max", "sorted", "enumerate",
    "zip", "map", "filter", "open", "abs", "round", "isinstance", "super",
    "def", "class", "return", "if", "elif", "else", "for", "while", "in",
    "not", "and", "or", "is", "import", "from", "as", "try", "except",
    "finally", "raise", "with", "lambda", "yield", "break", "continue",
    "pass", "global", "nonlocal", "True", "False", "None", "self"
  ],
  javascript: [
    "console", "function", "let", "const", "var", "return", "if", "else",
    "for", "while", "class", "new", "this", "typeof", "instanceof",
    "true", "false", "null", "undefined", "async", "await", "try", "catch",
    "finally", "throw", "import", "export", "default", "from", "of", "in",
    "map", "filter", "reduce", "forEach", "push", "length", "Math", "JSON"
  ],
  "c++": [
    "int", "float", "double", "char", "bool", "void", "auto", "const",
    "static", "class", "struct", "public", "private", "protected",
    "return", "if", "else", "for", "while", "do", "switch", "case",
    "break", "continue", "namespace", "using", "std", "cout", "cin",
    "endl", "vector", "string", "include", "new", "delete", "nullptr",
    "true", "false", "try", "catch", "throw", "template", "typename"
  ],
  go: [
  "func", "package", "import", "var", "const", "type", "struct", "interface",
  "return", "if", "else", "for", "range", "switch", "case", "break",
  "continue", "go", "chan", "select", "defer", "map", "nil", "true", "false",
  "fmt", "Println", "Printf", "make", "len", "append", "error"
  ],
  java: [
    "public", "private", "protected", "class", "interface", "extends",
    "implements", "static", "final", "void", "int", "double", "float",
    "boolean", "char", "String", "return", "if", "else", "for", "while",
    "new", "this", "super", "try", "catch", "finally", "throw", "throws",
    "import", "package", "System", "out", "println", "true", "false", "null"
  ],
  rust: [
    "fn", "let", "mut", "const", "struct", "enum", "impl", "trait", "pub",
    "use", "mod", "return", "if", "else", "match", "for", "while", "loop",
    "break", "continue", "true", "false", "None", "Some", "Ok", "Err",
    "println!", "vec!", "String", "Vec", "Option", "Result", "self", "Self"
  ]
};