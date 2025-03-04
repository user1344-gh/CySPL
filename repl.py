import run
import sys

def run_repl():
    while 1:
        inp = input("> ")
        res = run.run(inp, 2)
        if res[1]:
            print(res[1], file=sys.stderr)
        elif res[0]:
            print(res[0])
