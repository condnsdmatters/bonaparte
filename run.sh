#!/bin/bash

function get_yamls()
    mkdir -p indexes yamls
    for file in $(cat $1); do 
      pip install $file
      python  bonaparte/subpackage.py $file
      make singlehtml
      mv index.rst indexes/$file.done
      pip uninstall $file
    done

get_yamls top_modules.txt
