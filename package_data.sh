#!/bin/bash

function package_data(){
  echo "packaging..."
  TSTAMP=$(date +"_%m%d_%H%M")
  DIR="data.bonaparte.$TSTAMP"
  mkdir -p  $DIR/indexes/ $DIR/data/short $DIR/data/full $DIR/_raw/src 

  for file in $(ls indexes| grep ".file.done"); do
    cp indexes/$file $DIR/indexes/${file%$".done"}
  done

  cp yamls/*.short.yaml $DIR/data/short/
  cp yamls/*.yaml $DIR/data/full/
  rm -f $DIR/data/full/*.short.yaml

  ls $DIR/data/short | sed 's/.short.yaml//' > $DIR/module_contents.txt

  cp modules.txt $DIR/_raw/src/modules.txt
  cp requirements.txt $DIR/_raw/src/requirements.txt
  rsync -r venv/lib/python3.6/site-packages $DIR/_raw/src/
  echo "archiving..."
  tar -czf $DIR/_raw/src.$TSTAMP.tar.gz $DIR/_raw/src
  rm -rf $DIR/_raw/src

  printf "#README.md \nBonaparte data collection package.\n Collection stamp= $TSTAMP"> $DIR/README.md
}

package_data
