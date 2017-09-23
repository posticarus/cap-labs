grammar AritPlot;

prog:
      statement+ EOF            #statementList
    ;

statement:
      expr SCOL                 #exprInstr
    | 'set' ID '=' expr SCOL    #assignInstr
    | printplot=(PRINT|PLOT) expr ',' expr 'for' ID '=' expr '..' expr ('by' expr)? SCOL #printPlotInstr
    | 'quit' SCOL  #quitInstr
    ;

expr:
	expr mdop=(MULT | DIV) expr       #multiplicationExpr
    | expr pmop=(PLUS | MINUS) expr     #additiveExpr
    | atom                              #atomExpr
    ;

atom:
      (INT | FLOAT)             #numberAtom
    | ID                        #idAtom
    | '(' expr ')'              #parens
    ;


COS :       'cos';
SIN :       'sin';
SCOL :      ';';
PLUS :      '+';
MINUS :     '-';
MULT :      '*';
DIV :       '/';
PRINT :     'print';
PLOT :      'plot';
ID:         [a-zA-Z_] [a-zA-Z_0-9]*;

INT:        [0-9]+;


FLOAT: [0-9]+;

COMMENT:    '#' ~[\r\n]* -> skip;
NEWLINE:    '\r'? '\n' -> skip;
WS  :       (' '|'\t')+  -> skip;
