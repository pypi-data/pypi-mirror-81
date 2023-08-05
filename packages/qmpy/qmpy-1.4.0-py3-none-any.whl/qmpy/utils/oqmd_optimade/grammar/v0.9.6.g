// optimade v0.9.6 grammar spec in lark grammar format

start: KEYWORD expression
KEYWORD: "filter=" | "filter ="
expression: [expression CONJUNCTION] term 
term: [term CONJUNCTION] atom | "(" [term CONJUNCTION] term

atom: [NOT] comparison 

comparison: VALUE OPERATOR VALUE [")"] | VALUE OPERATOR "'" (combined)* "'"
OPERATOR: /<=?|>=?|!?=/

combined: VALUE ", " | VALUE "," | VALUE

VALUE: CNAME | SIGNED_FLOAT | SIGNED_INT | ESCAPED_STRING

CONJUNCTION: AND | OR
AND: /and/i
OR: /or/i
NOT: /not/i
%import common.CNAME
%import common.SIGNED_FLOAT
%import common.SIGNED_INT
%import common.ESCAPED_STRING
%import common.WS_INLINE
%ignore WS_INLINE