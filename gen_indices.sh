#!/bin/bash

function gen_indices(){
    mkdir -p indexes yamls
    
    echo "pip installing..."
    for module in $(cat $1); do
      echo "... $module"  
      pip3 -q install $module
    done
    echo "generating index files"
    python3 bonaparte/subpackage.py
    for new_file in $(ls indexes/*.file); do 
      if [ -f ./$new_file.done ]; then
        rm $new_file
      fi
    done
    ls indexes/*.file
}

gen_indices modules.txt
