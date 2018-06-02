# from pyaml import load
from yaml import load, dump
import os

def count_yamls():
    files = os.listdir("../yamls/")
    
    arg_count = 0
    func_count = 0 

    for f in files:
        if f.endswith(".short.yaml"):
            with open("../yamls/"+f, "r") as g:
                data = load(g)
   
            for k,v  in data.items():
                func_count += 1
                arg_count += len(v["arg_info"])
    print("Funcs: {}, Args: {}".format(func_count, arg_count))



if __name__=="__main__":
    count_yamls()