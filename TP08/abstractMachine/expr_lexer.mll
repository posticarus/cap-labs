{
(* digmips_lexer.mll *)
(* Analyseur lexical pour digmips*)
  open Expr_grammar
  open Lexing
  exception Eof 
}
  
let digit = ['0' - '9']
let integer_constant = digit+ (*    = *)
let nondigit = ['_' 'a'-'z' 'A'-'Z']
let newline = "\n" | "\r" | "\r\n"

let identifier =
  nondigit (nondigit | digit)*
			 
rule token = parse
| newline { Localizing.next_line lexbuf; token lexbuf }
| [' ' '\t' ] { token lexbuf }

| integer_constant { TK_INT (int_of_string (Lexing.lexeme lexbuf)) }
| '+'        { TK_PLUS }
| "let"      { TK_LET }
| "fun"      { TK_FUN }
| "in"       { TK_IN }
| "="        { TK_EQUAL  }
| "->"       { TK_ARROW  }
| "("      { TK_LPAREN  }
| ")"      { TK_RPAREN  }
| "rec"      { TK_REC  }
| identifier { TK_ID (Lexing.lexeme lexbuf) }
| eof { TK_EOF }
| _ {
  Format.printf "lexing error cannot lex %s at line %d\n"
  (Lexing.lexeme lexbuf)
  (Lexing.lexeme_end_p lexbuf).pos_lnum;
  failwith ""
}

