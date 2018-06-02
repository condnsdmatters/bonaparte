#!/bin/bash

function get_yamls(){
    for file in $(ls indexes |grep -v ".file.done"); do 
      echo "Parsing $file"
      cp indexes/$file index.rst 
      make singlehtml 2> /dev/null
      mv indexes/$file indexes/$file.done
      rm -f index.rst
    done
  }
get_yamls
