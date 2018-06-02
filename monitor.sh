#!/bin/bash

function monitor(){
    while true; do 
      args=$(egrep -r  "^        -" yamls/*short* | wc -l);
      done_files=$(ls indexes| grep -c file.done); 
      blank=$(egrep -r "^            desc: \[\]" yamls/*short* | wc -l); 
      most_recent=$(ls indexes | grep -v "file.done"|head -n 1); 
      tot=$(ls indexes | wc -l); 
      echo "Done: $done_files/$tot,     Args: $args, Blank: $blank, Current: $most_recent"; 
      sleep 3;
   done
}

monitor

