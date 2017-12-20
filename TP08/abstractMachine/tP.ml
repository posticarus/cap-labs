open Syntax

(* Compilation of expressions to machine code *)
let rec compile : expr -> code =
  function
  | Constant k -> [Cst k]
  | Addition (e1, e2) -> compile e1 @ compile e2 @ [Add]

  | _ -> Parser.fail "Not implemented."

(* Exception that should be raised by the machine when there is no transition from the current state *)     
exception No_transition

(* Transition function for the machine:
   maps a state to the next state in the evaluation *)
let transition (code, env, stack) : state = match code with
  | [] -> raise No_transition

  | Cst k :: rest -> (rest, env, VInt k :: stack)

  | Add :: rest -> begin match stack with
    | VInt k1 :: VInt k2 :: stack -> (rest, env, VInt (k1 + k2) :: stack)
    | _ -> Parser.fail "Add: Expected two ints on the stack."
  end

  | _ -> Parser.fail "Not implemented."

(* Builtins operations.
   Those operations are present in the initial environment when running code in [main.ml] 
*)
let builtins =
  ["print",
   VBuiltin ("print",
             (function
             | VInt k :: stack -> Printf.printf "%d\n" k; flush stdout; VInt 0 :: stack
             | _ -> failwith "expcted int"));
  ]
