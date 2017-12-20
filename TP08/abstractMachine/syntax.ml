(** Definition of the types for the syntaxes *)
  
(* The type of our variables *)
type variable = string
  
(* Syntax of the input language of terms. *)
type expr =
  (* Arithmetic fragment *)
  | Constant of int
  | Addition of expr * expr
      
  (* Let fragment *)
  | Variable of variable
  | Let of variable * expr * expr (* [Let (x, a, b)] stands for [let x = a in b] *)

  (* Functional fragment *)
  | Function of variable * expr
  | Application of expr * expr

(* Instruction of the machine *)
type instr =
  (* Arithmetic fragment *)
  | Cst of int
  | Add
      
  (* Let fragment *)
  | Access of variable
  | Let of variable
  | EndLet
      
  (* Functional fragment *)
  | Closure of variable * code
  | App
  | Ret

(* Code is just a list of instructions. *)      
and code = instr list
  
(* An environment is a (partial) map from variables to values. *)
type environment = (variable * value) list
(* Values that can be stored on the stack *)  
and value =
  | VInt of int
  | VClosure of string * code * environment
  | VBuiltin of string * (stack -> stack) (* A builtin (caml) function. The string denotes the name *)

(* Stacks *)      
and stack = value list

(* States of the machine *)
type state = code * environment * stack
