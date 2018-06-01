import pdb 
import inspect
import re
from collections import OrderedDict

from yaml import load, dump
import pyaml

NO_DOCSTRING_REG = re.compile("'''[^(''')]*'''", re.DOTALL)
YAML_PATH = "yamls/"

is_indented = lambda x: x.startswith(" ")
has_description = lambda args: any([bool(a["desc"]) for a in args.values()]) 

def export_to_yaml(what, fullname, code_object, lines):
    filename = "UNK"
    try: 
        filename = get_filename(code_object)
        pkg, name = get_pkg_and_funcname(fullname)
        src = get_src(code_object)
        sig, params = get_sig_and_params(code_object)
        param_info = get_param_info(params, lines, sig)
        
        if has_description(param_info):
            write_to_yaml(pkg, name, filename, src, sig, params, param_info, lines)

    except (OSError, TypeError) as e:
        log_error(what, filename, fullname, code_object, lines)

def get_filename(obj):
    return inspect.getfile(obj).split("site-packages")[-1]

def get_pkg_and_funcname(name):
    n = name.split(".")
    return n[0], n[-1]

def get_src(obj):
    full_src = inspect.getsource(obj)
    no_docstring = re.sub(NO_DOCSTRING_REG,"", full_src, count=1)
    return no_docstring

def get_sig_and_params(obj):
    sig = inspect.signature(obj)
    return str(sig), list(sig.parameters.keys())

def get_param_info(params, lines, sig):
    p_info = OrderedDict([(p, {"desc":[], "type":None}) for p in params ])
    
    current = None

    
    for l in lines:
        if l.startswith(":param"):
            s = l.split(":")
            param = s[1].replace("param ", "").replace("\\", "").replace("*", "").replace("=",'')
            if param in p_info:
                p_info[param]["desc"] = s[-1]
            elif "**" in sig:
                param = "**" + param
                p_info[param] = {"desc":s[-1], "type":None}
            current = "param"

        elif is_indented(l) and current == "param":
            if param in p_info:
                p_info[param]["desc"] += " " + l.strip()
            elif "**" in sig:
                param = "**" + param
                p_info[param]["desc"] += " " + l.strip()
                

        elif l.startswith(":type"):
            s = l.split(":")
            param = s[1].replace("type ", "").replace("\\", "").replace("*", "").replace("=",'')
            if param in p_info:
                p_info[param]["type"] = s[-1]
            elif "**" in sig:
                param = "**" + param
                p_info[param]["type"] = s[-1]
            current = "type"           
        elif is_indented(l) and current == "type":
            current = None
        else:
            current = None

    return p_info


def write_to_yaml(pkg, name, filename, src, sig, params, param_info, lines):
    full_record = OrderedDict([
        ("name", name),
        ("sig", sig),
        ("args", params),
        ("filename", filename),
        ("pkg", pkg),
        ("arg_info", param_info),
        ("docstring", "\n".join(lines)),
        ("src", src),
    ])

    short_record = OrderedDict([
        ("name", name),
        ("sig", sig),
        ("args", params),
        ("filename", filename),
        ("pkg", pkg),
        ("arg_info", param_info),
    ])

    with open(YAML_PATH + pkg+".yaml", "a") as f:
        f.write(pyaml.dump({filename+'--'+name: full_record}, indent=4))

    with open(YAML_PATH + pkg+".short.yaml", "a") as f:
        f.write(pyaml.dump({filename+'--'+name:short_record}, indent=4))

def log_error(what, filename, name, obj, lines):
    with open(YAML_PATH + "error.yaml", "a") as f:
        f.write(filename)
        f.write("\n")
        f.write(name)
        f.write("\n")
