(* Pretty-printers *)
open Syntax
  
let spr = Printf.sprintf
let rec expr = function
  | Constant n -> string_of_int n
  | Addition (e1, e2) -> spr "%s + %s" (expr e1) (expr e2)

  | Let (x, a, b) -> spr "let %s = %s in %s" x (expr a) (expr b)
  | Variable s -> s

  | Function (x, t) -> spr "(fun %s -> %s)" x (expr t)
  | Application (t, t') -> spr "%s %s" (expr t) (expr t')

(*  | LetRec (x, a, b) -> spr "let rec %s = %s in %s" x (expr a) (expr b)*)

let rec instr = function
  | Cst n -> spr "Cst %d" n
  | Add -> spr "Add"
     
  | Let s -> spr "Let %S" s
  | EndLet -> spr "EndLet"
  | Access s -> spr "Access %S" s

  | Closure (x, t) -> spr "Closure(%S, %s)" x (code t)
  | App -> "App"
  | Ret -> "Ret"

(* | Rec s -> spr "Rec %s" s*)
     
and code l = String.concat "; " (List.map instr l)

let rec value = function
  | VInt n -> string_of_int n
  | VClosure (x, t, e) ->
     Printf.sprintf "({%s}%s, [%s])"
       x (code t) (environment e)
  | VBuiltin (name, _) -> spr "<builtin:%s>" name
and environment e =
  String.concat "; "
    @@ List.map (fun (name, v) -> Printf.sprintf "%s=%s" name (value v)) e

let state (c, e, s) =
  Printf.sprintf "State: \n  Code: %s\n  Env: %s\n  Stack: %s\n"
    (code c)
    (environment e)
    (String.concat " · " @@ (List.map value s @ ["ε"]))
