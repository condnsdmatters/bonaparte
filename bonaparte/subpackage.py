import pkgutil
import site
import os

from collections import defaultdict

SITE_PACKAGES = site.getsitepackages()[0]

def get_submodules():
    path = SITE_PACKAGES + "/"


    pkg_list = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                mod_root = root.replace(SITE_PACKAGES + "/", "").replace("/",".")
                if mod_root:
                    modname = mod_root  + "." + f.split(".py")[0]
                else:
                    modname = f.split(".py")[0]
                pkg_list.append(modname)
    return pkg_list



def to_directive_string(submodules):
    directive = """.. automodule:: {}\n    :members:"""
    dir_string = [directive.format(s) for s in submodules]

    return "\n".join(dir_string)


def to_index_file(dir_string):
   return '''
 .. TRYIT documentation master file, created by sphinx-quickstart on Fri Jun  1 16:03:15 2018.
You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.

Welcome to TRYIT's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

{}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

'''.format(dir_string)


def write_submodules_to_files(submodules):
    directories = defaultdict(list)
    for s in submodules:
        directories[s.split(".")[0]].append(s)
    for k,v in directories.items():
        with open("indexes/{}.file".format(k) , 'w') as f:
            f.write(to_index_file(to_directive_string(v)))

if __name__=="__main__":
    submodules = get_submodules()
    write_submodules_to_files(submodules)
    # file = to_index_file(to_directive_string(submodules))
    # with open("index.rst", 'w') as f:
    #     f.write(file)
