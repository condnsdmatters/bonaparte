# Bonaparte

Bonaparte hijacks Sphinx's documentation plugin Napoleon, to allow you to print docstrings, parameter descriptions, and  source to a yaml file.


### To Collect Data
You will be installing modules via pip, and then using Sphinx's docstring parser to parse these modules. This saves the hassle of having to clone and build source.

1. Create a virtualenvironment, and install: sphinx, pyaml
2. Create (or use the file) modules.txt It should have the list of names of modules you will install with pip.
3. _run_: `./gen_indices.sh`  - this will pip install modules, and generate files for sphinx (in `indexes`)
4. _run_: `./run.sh` - this will take the files in `indexes` and start parsing
5. _run_: `./package_data` - this will collect all the data and original source and bundle it for you.

Throughout the `run.sh` phase you can monitor the progress crudely by just running `monitor.sh` in another window.
