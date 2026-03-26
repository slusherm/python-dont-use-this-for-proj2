import sys
import time
import clingo

def solve(instance_file: str) -> None:
    version = ".".join(str(x) for x in clingo.__version__.split("."))
    print(f"clingo version {clingo.__version__}")
    print(f"Reading from {instance_file}")
    print("Solving...")
 
    ctl = clingo.Control(["--models=1"])
    ctl.add("base", [], SUDOKU_ENCODING)
 
    try:
        with open(instance_file) as fh:
            instance_facts = fh.read()
        ctl.add("base", [], instance_facts)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
 
    ctl.ground([("base", [])])
 
    answer_count = 0
    atoms_line = ""
 
    wall_start = time.time()
    solve_start = time.time()
    first_model_time = 0.0
 
    with ctl.solve(yield_=True) as handle:
        solve_start = time.time()
        for model in handle:
            answer_count += 1
            first_model_time = time.time() - solve_start
            atoms = sorted(str(atom) for atom in model.symbols(shown=True))
            atoms_line = " ".join(atoms)
            print(f"Answer: {answer_count}")
            print(atoms_line)
        result = handle.get()
 
    wall_end = time.time()
    total_wall = wall_end - wall_start
    solve_elapsed = wall_end - solve_start
    unsat_time = solve_elapsed - first_model_time if answer_count > 0 else solve_elapsed
 
    if result.satisfiable:
        print("SATISFIABLE")
    elif result.unsatisfiable:
        print("UNSATISFIABLE")
    else:
        print("UNKNOWN")
 
    print()
    
    models_str = f"{answer_count}+" if result.satisfiable else str(answer_count)
    print(f"Models       : {models_str}")
    print(f"Calls        : 1")
    print(
        f"Time         : {total_wall:.3f}s "
        f"(Solving: {solve_elapsed:.2f}s "
        f"1st Model: {first_model_time:.2f}s "
        f"Unsat: {unsat_time:.2f}s)"
    )
    print(f"CPU Time     : {total_wall:.3f}s")
    print()
 
 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <instance_file>", file=sys.stderr)
        sys.exit(1)
    solve(sys.argv[1])