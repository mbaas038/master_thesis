#!/bin/bash

# taken from dedode_spm_enca.sh
# does detok, norm, iunorm

source `dirname "$0"`/vars.sh

SL=en
TL=nl


GPUS=0
MDIR=/data/s3212262/thesis_data/models/OpenSubtitles/context_1000/msent-ennl-BPE96000-1-27000
MODEL=$MDIR/models/model.npz
BEAM=$1; shift
NORM=$1; shift
BATCH=$1; shift
WORKSPACE=$1

mkdir -p $MDIR/decode/


function seg_apply {
	spm_ini

	cat $TESTDIR/test.it.1000.dec.en \
	| $SPM/spm_encode --model=$MDIR/spm/spm.model \
	--vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
	> $MDIR/spm/test.it.dec.spm.$SL

        cat $TESTDIR/test.you.1000.dec.en \
        | $SPM/spm_encode --model=$MDIR/spm/spm.model \
        --vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
        > $MDIR/spm/test.you.dec.spm.$SL
}


function decode {
	marian_ini

	cat $MDIR/spm/test.it.dec.spm.$SL | \
	$MARIAN_DECODER \
		--models $MODEL \
		-v $MDIR/spm/vocab.$SL$TL.yml $MDIR/spm/vocab.$SL$TL.yml \
		-b $BEAM --normalize $NORM \
		--mini-batch $BATCH --maxi-batch-sort src --maxi-batch 100 -w $WORKSPACE \
		--log $MDIR/decode/$OUTNAME.log \
		> $MDIR/decode/test.it.dec.spm.$TL

	cat $MDIR/decode/test.it.dec.spm.$TL \
	    | sed 's/ //g' \
	    | sed 's/▁/ /g' \
	    | sed 's/^ //' \
		> $MDIR/decode/test.it.dec.$TL

        cat $MDIR/spm/test.you.dec.spm.$SL | \
        $MARIAN_DECODER \
                --models $MODEL \
                -v $MDIR/spm/vocab.$SL$TL.yml $MDIR/spm/vocab.$SL$TL.yml \
                -b $BEAM --normalize $NORM \
                --mini-batch $BATCH --maxi-batch-sort src --maxi-batch 100 -w $WORKSPACE \
                --log $MDIR/decode/$OUTNAME.log \
                > $MDIR/decode/test.you.dec.spm.$TL

        cat $MDIR/decode/test.you.dec.spm.$TL \
            | sed 's/ //g' \
            | sed 's/▁/ /g' \
            | sed 's/^ //' \
                > $MDIR/decode/test.you.dec.$TL

}


seg_apply
decode

