open Syntax
type state = {
  bindings: Syntax.environment;
  debug: bool;
}


let run {bindings; debug} code =
  let rec loop state =
    try
      let state = TP.transition state in
      if debug then
        Printf.eprintf "→ %s\n%!" @@ Printers.state state;
      loop state
    with TP.No_transition -> state
  in
  if debug then
    Printf.eprintf "  %s\n%!" @@ Printers.state (code, bindings, []);
  let (_, _, st) = loop (code, bindings, []) in
  match st with
  | [] -> Parser.fail "No value left on the stack."
  | t :: _ -> t


     
let rec process line state =
  Scanf.sscanf line "%s %[^\n]" (fun s args ->
    match s with
    | "" -> state
    | "c" | "compile" ->
       let expr = Parser.expr args in
       print_endline (Printers.code (TP.compile expr));
       state
    | "r" | "run" ->
       let code, _ = Parser.code args in
       print_endline (Printers.value (run state code));
       state
    | "cr" | "compile-run" ->
       let expr = Parser.expr args in
       print_endline (Printers.value (run state (TP.compile expr)));
       state
    | "q" | "exit" -> exit 0
    | "set" ->
       if args = "debug" then { state with debug = true }
       else begin
         try Scanf.sscanf args "debug %s" (fun b ->
           if b = "true" then { state with debug = true } else state)
         with _ -> Parser.fail "set debug [true|false]"
       end
    | "let" ->
       (try 
          Scanf.sscanf args "%s = %[^\n]"
            (fun name expr ->
              let binding = name, run state (TP.compile (Parser.expr expr)) in
              { state with bindings = binding :: state.bindings })
        with Scanf.Scan_failure _ -> Parser.fail "Syntax error, usage: [let x = e]")
    | "source" | "s" -> source args state
    | _ -> Parser.fail "Unknown command `%s'\n%!" s)
and source fname state = try
  let fd = open_in fname in
  let () = Localizing.current_file_name := fname;
    Localizing.current_line_num := 0; Localizing.current_line_start_pos := 0;
  in
  let rec line state =
    try line (process (input_line fd) state)
    with End_of_file -> state
  in
  let v = line state in
  close_in fd;
  Localizing.current_file_name := "<stdin>";
  v
  with Sys_error _ -> Parser.fail "File `%s' not found." fname

let rec toplevel state =
  Printf.printf "> "; flush stdout;
  let input = input_line stdin in
  try toplevel (process input state)
  with Failure "err" -> toplevel state

let state = ref { bindings = TP.builtins; debug = false }
  
let _ = Arg.
  (parse
     (align
        ["-d", Unit (fun () -> state := { !state with debug = true }), " Set debug mode";])
     (fun filename -> state := source filename !state)
     "A toplevel for a virtual machine. Commands:
compile <expr> or c <expr>      : compiles <expr> and outputs the bytecode.
run <code> or r <code>          : runs code <code>.
compile-run <expr> or cr <expr> : compile <expr> and run the resulting code.
q                               : quits
source <filename>               : process <filename> as if it was typed on the toplevel
set debug [true|false]          : sets the debug flag.
let <var> = <expr>              : compiles and run <expr> and binds the resulting value to x in the ambient environment so it is available to further expressions.\n")
let _ = toplevel !state
    
  
