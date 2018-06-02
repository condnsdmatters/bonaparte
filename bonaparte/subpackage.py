import pkgutil
import site
import os

SITE_PACKAGES = site.getsitepackages()[0]

def get_submodules(package):
    path = SITE_PACKAGES + "/" + package


    pkg_list = [package]
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                modname = root.replace(SITE_PACKAGES + "/", "").replace("/",".") + "." + f.split(".py")[0]
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


if __name__=="__main__":
    import sys
    file = to_index_file(to_directive_string(get_submodules(sys.argv[2])))
    with open("index.rst", 'w') as f:
        f.write(file)
