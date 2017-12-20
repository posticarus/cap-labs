%token  <string>  TK_ID
%token  <int>     TK_INT
%token            TK_FUN TK_ARROW TK_PLUS TK_LET TK_EQUAL TK_IN TK_LPAREN TK_RPAREN TK_EOF TK_PHANTOM TK_REC

%type <Syntax.expr> expr main
%start main
%nonassoc TK_LET TK_IN TK_FUN TK_ARROW
%left TK_PLUS
%nonassoc TK_INT TK_ID
%nonassoc TK_LPAREN
%left TK_PHANTOM
%%

expr:
   | TK_LPAREN expr TK_RPAREN { $2 }

   | TK_INT { Syntax.Constant $1 }
   | expr TK_PLUS expr { Syntax.Addition ($1, $3) }

   | TK_ID { Syntax.Variable $1 }
   | TK_LET TK_ID TK_EQUAL expr TK_IN expr { Syntax.Let ($2, $4, $6) }


   | TK_FUN list(TK_ID)  TK_ARROW expr
       { List.fold_right (fun x term -> Syntax.Function (x, term)) $2 $4 }
   | expr expr %prec TK_PHANTOM { Syntax.Application ($1, $2) }

(*   | TK_LET TK_REC TK_ID TK_EQUAL expr TK_IN expr { Syntax.LetRec ($3, $5, $7) } *)


main:
   | expr TK_EOF { $1 }





(* %token  <string>  TK_ID *)
(* %token  <int>     TK_INT *)
(* %token            TK_FUN TK_ARROW TK_PLUS TK_LET TK_EQUAL TK_IN TK_LPAREN TK_RPAREN TK_EOF TK_PHANTOM *)

(* %type <Syntax.expr> expr main *)
(* %start main *)
(* %left TK_PHANTOM *)
(* %left TK_IN TK_ARROW *)
(* %left TK_PLUS *)
(* %nonassoc TK_INT TK_ID *)
(* %nonassoc TK_LPAREN TK_RPAREN *)
(* %% *)

(* compound: *)
(* | TK_LET TK_ID TK_EQUAL compound TK_IN compound { Syntax.Let ($2, $4, $6) } *)

(* | TK_FUN list(TK_ID)  TK_ARROW compound *)
(*   { List.fold_right (fun x term -> Syntax.Function (x, term)) $2 $4 } *)
(* | expr { $1 } *)

(* expr: *)
(* | expr simple_expr { Syntax.Application ($1, $2) } *)
(* | simple_expr { $1 } *)
    
(* simple_expr: *)
(* | TK_INT { Syntax.Constant $1 } *)
(* | expr TK_PLUS expr { Syntax.Addition ($1, $3) } *)
(* | TK_ID { Syntax.Variable $1 } *)
(* | TK_LPAREN compound TK_RPAREN { $2 } *)

(* main: *)
(* | compound TK_EOF { $1 } *)

