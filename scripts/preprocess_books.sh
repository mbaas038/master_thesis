#!/bin/bash

GIZA_DIR=~/thesis/Software/giza-pp/GIZA++-v2
UDPIPE=~/thesis/Software/udpipe/udpipe-1.2.0-bin/bin-linux64/udpipe
MOSES=~/thesis/Software/mosesdecoder/scripts
UD_MODEL_DIR=~/thesis/Software/udpipe/models
BOOKS_DIR=/data/s3212262/thesis_data/Books

function word_alignment {
    d="$1"
    cd "$d"
    echo "Aligning en<->nl..."
    mkdir -p "giza_out"
    $GIZA_DIR/plain2snt.out "en.tok.clean" "nl.tok.clean"
    $GIZA_DIR/snt2cooc.out "en.tok.clean.vcb" "nl.tok.clean.vcb"  "en.tok.clean_nl.tok.clean.snt"  > "corp.cooc"
    $GIZA_DIR/GIZA++ -S "en.tok.clean.vcb" -T "nl.tok.clean.vcb" -C "en.tok.clean_nl.tok.clean.snt"  -CoocurrenceFile "corp.cooc" -outputpath "giza_out/"
    echo "Aligning en<->nl... [done]"

    # clean up unnecessary files
    rm *.vcb
    rm *.snt
    rm corp.cooc
    mv giza_out/*.A3.final en_nl.align
    rm -rf giza_out
    cd ..

}

function pos_tag {
    d="$1"
    echo "Tagging English..."
    $UDPIPE --input=horizontal --parse --tag $UD_MODEL_DIR/english-ewt-ud-2.5-191206.udpipe "$d/en.tok.clean" > "$d/en.tag"
    echo "Tagging English... [done]"
    echo "Tagging Dutch..."
    $UDPIPE --input=horizontal --parse --tag $UD_MODEL_DIR/dutch-alpino-ud-2.5-191206.udpipe "$d/nl.tok.clean" > "$d/nl.tag"
    echo "Tagging Dutch... [done]"
}

for bookdir in $BOOKS_DIR/*/;
do
  echo "------------------------------"
  echo "Processing $bookdir..."
  if [ ! -f "$bookdir/en.tag" ]; then
    pos_tag "$bookdir"
  fi
  if [ ! -f "$bookdir/en_nl.align" ]; then
    word_alignment "$bookdir"
  fi
  echo "Processing $bookdir... [done]"
  echo "------------------------------"
done
