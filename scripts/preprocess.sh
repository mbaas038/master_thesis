#!/bin/bash

MOSESSCRIPTS=~/thesis/Software/mosesdecoder/scripts
GIZA_DIR=~/thesis/Software/giza-pp/GIZA++-v2
UDPIPE=~/thesis/Software/udpipe/udpipe-1.2.0-bin/bin-linux64/udpipe
UD_MODEL_DIR=~/thesis/Software/udpipe/models
TED_DATA_DIR=/data/s3212262/thesis_data/TED
SUB_DATA_DIR=/data/s3212262/thesis_data/OpenSubtitles/raw


function tokenize_data {
	echo TED Data: tokenizing en...
    ${MOSESSCRIPTS}/tokenizer/tokenizer.perl -no-escape -l en < ${TED_DATA_DIR}/TED2013.en-nl.en > ${TED_DATA_DIR}/TED2013.en-nl.tok.en
    echo TED Data: tokenizing en... done!
    echo TED Data: tokenizing nl...
    ${MOSESSCRIPTS}/tokenizer/tokenizer.perl -no-escape -l nl < ${TED_DATA_DIR}/TED2013.en-nl.nl > ${TED_DATA_DIR}/TED2013.en-nl.tok.nl
    echo TED Data: tokenizing nl... done!

    echo Subtitle Data: tokenizing en...
    ${MOSESSCRIPTS}/tokenizer/tokenizer.perl -no-escape -l en < ${SUB_DATA_DIR}/OpenSubtitles.en-nl.en > ${SUB_DATA_DIR}/OpenSubtitles.en-nl.tok.en
    echo Subtitle Data: tokenizing en... done!
    echo Subtitle Data: tokenizing nl...
    ${MOSESSCRIPTS}/tokenizer/tokenizer.perl -no-escape -l nl < ${SUB_DATA_DIR}/OpenSubtitles.en-nl.nl > ${SUB_DATA_DIR}/OpenSubtitles.en-nl.tok.nl
    echo Subtitle Data: tokenizing nl... done!
}

function word_alignment {
    mkdir -p $TED_DATA_DIR/giza_out
    $GIZA_DIR/plain2snt.out $TED_DATA_DIR/TED2013.en-nl.tok.en $TED_DATA_DIR/TED2013.en-nl.tok.nl
    $GIZA_DIR/snt2cooc.out $TED_DATA_DIR/TED2013.en-nl.tok.en.vcb $TED_DATA_DIR/TED2013.en-nl.tok.nl.vcb  $TED_DATA_DIR/TED2013.en-nl.tok.en_TED2013.en-nl.tok.nl.snt  > $TED_DATA_DIR/corp.cooc
    $GIZA_DIR/GIZA++ -S $TED_DATA_DIR/TED2013.en-nl.tok.en.vcb -T $TED_DATA_DIR/TED2013.en-nl.tok.nl.vcb -C $TED_DATA_DIR/TED2013.en-nl.tok.en_TED2013.en-nl.tok.nl.snt  -CoocurrenceFile $TED_DATA_DIR/corp.cooc -outputpath $TED_DATA_DIR/giza_out/

    mkdir -p $SUB_DATA_DIR/giza_out
    $GIZA_DIR/plain2snt.out $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.en $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.nl
    $GIZA_DIR/snt2cooc.out $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.en.vcb $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.nl.vcb  $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.en_OpenSubtitles.en-nl.tok.nl.snt  > $SUB_DATA_DIR/corp.cooc
    $GIZA_DIR/GIZA++ -S $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.en.vcb -T $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.nl.vcb -C $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.en_OpenSubtitles.en-nl.tok.nl.snt  -CoocurrenceFile $SUB_DATA_DIR/corp.cooc -outputpath $SUB_DATA_DIR/giza_out/
}

function pos_tag {
    $UDPIPE --tokenize --tokenizer=presegmented --tag $UD_MODEL_DIR/english-ewt-ud-2.5-191206.udpipe $TED_DATA_DIR/TED2013.en-nl.tok.en > $TED_DATA_DIR/TED2013.en-nl.tag.en
    $UDPIPE --tokenize --tokenizer=presegmented --tag $UD_MODEL_DIR/dutch-alpino-ud-2.5-191206.udpipe $TED_DATA_DIR/TED2013.en-nl.tok.nl > $TED_DATA_DIR/TED2013.en-nl.tag.nl

    $UDPIPE --tokenize --tokenizer=presegmented --tag $UD_MODEL_DIR/english-ewt-ud-2.5-191206.udpipe $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.en > $SUB_DATA_DIR/OpenSubtitles.en-nl.tag.en
    $UDPIPE --tokenize --tokenizer=presegmented --tag $UD_MODEL_DIR/dutch-alpino-ud-2.5-191206.udpipe $SUB_DATA_DIR/OpenSubtitles.en-nl.tok.nl > $SUB_DATA_DIR/OpenSubtitles.en-nl.tag.nl
}

pos_tag
