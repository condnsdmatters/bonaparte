#!/bin/bash

function gen_indices(){
    mkdir -p indexes yamls
    
    echo "installing modules.tx"
    pip3 -q install -r $1
    echo "generating index files"
    python3 bonaparte/subpackage.py
    for new_file in $(ls indexes/*.file); do 
      if [ -f ./$new_file.done ]; then
        rm $new_file
      fi
    done
}

gen_indices modules.txt
