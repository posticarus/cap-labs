(* Parsers *)
let fail fmt = Printf.kprintf (fun s -> prerr_endline s; failwith "err") fmt
  
let expr s =
  let lexbuf = Lexing.from_string (s^"\n") in
  try
    Expr_grammar.main Expr_lexer.token lexbuf
  with e ->
    let msg =  (Printexc.to_string e) in 
    fail "%s at %s" msg Localizing.(extent_to_string (extent lexbuf))

let rec instr s =
  try
    Scanf.sscanf s "%s %[^\n]" (fun instr rest ->
      let wrap_fmt fmt f =
        try
          Scanf.sscanf rest (fmt ^^ "%[^\n]") (fun a r -> f a, r)
        with _ -> fail "Invalid arguments at %s for instr %s" rest instr
      in
      match instr with
      | "Cst" -> wrap_fmt "%d" (fun n -> Syntax.Cst n)
      | "Add" -> Syntax.Add, rest

      | "Access" -> wrap_fmt "%S" (fun s -> Syntax.Access s)
      | "Let" -> wrap_fmt "%S" (fun s -> Syntax.Let s)
      | "EndLet" -> Syntax.EndLet, rest
        
      | "Closure" ->
         Scanf.sscanf rest "(%S, %[^\n]" (fun name cont ->
           let code, rest = code cont in
           Scanf.sscanf rest " )%[^\n]" (fun rest ->
             Syntax.Closure (name, code), rest))
      | "App" -> Syntax.App, rest

      | _ -> fail "Invalid instruction: %s" instr)
  with _ -> fail "Instruction expected at `%s'." s
    
and code s =
  let instr, rest = instr s in
  if rest = "" then [instr], ""
  else
    try 
      Scanf.sscanf rest "; %[^\n]" (fun rest ->
        match rest.[0] with
        | 'a'..'z' | 'A' .. 'Z' ->
           let code, rest = code rest in
           instr :: code, rest
        | _ -> [instr], rest)
    with _ -> fail "Semicolon expected at %s" rest
    
