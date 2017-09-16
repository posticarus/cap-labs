grammar Arit2;

// CAP@ENSL, LAB 02, arit evaluator

@header {
#header - mettre les variables globales 
import sys
idTab = {};
}

prog: ID ;


ID : ('a'..'z'|'A'..'Z')+;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
INT: '0'..'9'+;
NEWLINE: [\n]+;
