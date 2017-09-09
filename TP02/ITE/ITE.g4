grammar ITE;

prog: stmt;

stmt : ifStmt | ID ;

ifStmt : 'if' ID stmt ('else' stmt)? ;

//ifStmt : 'if' ID stmt ('else' stmt | {_input.LA(1) != ELSE}?);
//ELSE : 'else';


ID : [a-zA-Z]+;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

