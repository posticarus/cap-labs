grammar Arit;

@header {
#header - mettre les variables globales
idTab = {};
}

@members {
# members - relire la doc
}

prog:
      statement+ EOF            #statementList
    ;

statement:
      expr SCOL                 #exprInstr
    | 'set' ID '=' expr SCOL    #assignInstr
    ;

expr:
	expr mdop=(MULT | DIV) expr     #multiplicationExpr
    | expr pmop=(PLUS | MINUS) expr     #additiveExpr
    | atom                              #atomExpr
    ;

atom:
      INT                       #numberAtom
    | ID                        #idAtom
    | '(' expr ')'              #parens
    ;


SCOL :      ';';
PLUS :      '+';
MINUS :     '-';
MULT :      '*';
DIV :       '/';
ID:         [a-zA-Z_] [a-zA-Z_0-9]*;

INT:        [0-9]+;

COMMENT:    '#' ~[\r\n]* -> skip;
NEWLINE:    '\r'? '\n' -> skip;
WS  :       (' '|'\t')+  -> skip;
