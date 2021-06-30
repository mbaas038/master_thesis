#!/bin/bash

source `dirname "$0"`/vars.sh

SL=en
TL=nl


MDIR=$WORKDIR/msent-$SL$TL-BPE48000-1-27000-test/

function seg_apply {
        spm_ini

        cat $TESTDIR/test.it.0.$SL \
        | $SPM/spm_encode --model=$MDIR/spm/spm.model \
        --vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
        > $MDIR/spm/test.it.spm.$SL
        
        cat $TESTDIR/test.it.0.$TL \
        | $SPM/spm_encode --model=$MDIR/spm/spm.model \
        --vocabulary=$MDIR/spm/spm.vocab.$TL --vocabulary_threshold=50 \
        > $MDIR/spm/test.it.spm.$TL

        cat $TESTDIR/test.you.0.$SL \
        | $SPM/spm_encode --model=$MDIR/spm/spm.model \
        --vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
        > $MDIR/spm/test.you.spm.$SL

        cat $TESTDIR/test.you.0.$TL \
        | $SPM/spm_encode --model=$MDIR/spm/spm.model \
        --vocabulary=$MDIR/spm/spm.vocab.$TL --vocabulary_threshold=50 \
        > $MDIR/spm/test.you.spm.$TL

}

function score {
  marian_ini

  $MARIAN_SCORER \
  --model $MDIR/models/model.npz \
  --vocabs $MDIR/spm/vocab.$SL$TL.yml $MDIR/spm/vocab.$SL$TL.yml \
  --train-sets $MDIR/spm/test.it.spm.$SL $MDIR/spm/test.it.spm.$TL \
  --output $MDIR/scores/test.it.scores

  $MARIAN_SCORER \
  --model $MDIR/models/model.npz \
  --vocabs $MDIR/spm/vocab.$SL$TL.yml $MDIR/spm/vocab.$SL$TL.yml \
  --train-sets $MDIR/spm/test.you.spm.$SL $MDIR/spm/test.you.spm.$TL \
  --output $MDIR/scores/test.you.scores

}

mkdir -p $MDIR/scores/
seg_apply
score

