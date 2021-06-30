#!/bin/bash

# taken from dedode_spm_enca.sh
# does detok, norm, iunorm

source `dirname "$0"`/vars.sh

SL=en
TL=nl


GPUS=0
MDIR=/data/s3212262/thesis_data/models/TED/context_400/msent-ennl-BPE2000-1-27000
MODEL=$MDIR/models/model.npz
BEAM=$1; shift
NORM=$1; shift
BATCH=$1; shift
WORKSPACE=$1

mkdir -p $MDIR/decode/


function seg_apply {
	spm_ini

	cat $TESTDIR/normal.400.en \
	| $SPM/spm_encode --model=$MDIR/spm/spm.model \
	--vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
	> $MDIR/spm/normal.dec.spm.$SL
}


function decode {
	marian_ini

	cat $MDIR/spm/normal.dec.spm.$SL | \
	$MARIAN_DECODER \
		--models $MODEL \
		-v $MDIR/spm/vocab.$SL$TL.yml $MDIR/spm/vocab.$SL$TL.yml \
		-b $BEAM --normalize $NORM \
		--mini-batch $BATCH --maxi-batch-sort src --maxi-batch 100 -w $WORKSPACE \
		--log $MDIR/decode/$OUTNAME.log \
		> $MDIR/decode/normal.dec.spm.$TL

	cat $MDIR/decode/normal.dec.spm.$TL \
	    | sed 's/ //g' \
	    | sed 's/▁/ /g' \
	    | sed 's/^ //' \
		> $MDIR/decode/normal.dec.$TL

}


seg_apply
decode

