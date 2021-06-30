#!/bin/bash

# Model ENNL sentence-based
# Based on ENCA's model_lit.sh

# Parameters: NBPE, SEED, NEPOCHS, WORKSPACE

source `dirname "$0"`/vars.sh

#---------
GPUS=0
#---------

#---------
SL=en
TL=nl
NBPE=$1
N=$2
SEED=$N$N$N$N$N
EPOCHS=$3
WORKSPACE=$4
#---------


MDIR=$WORKDIR/msent-$SL$TL-BPE$NBPE-$N-$WORKSPACE
mkdir -p $MDIR
mkdir -p $MDIR/spm



# Fails with 16GB (works with 32GB)
function seg_train {
	spm_ini
	
	$SPM/spm_train \
	--input=$DATADIR/train/train4spm.$TL,$DATADIR/train/train4spm.$SL \
	--model_prefix=$MDIR/spm/spm \
	--vocab_size=$NBPE \
	--character_coverage=1.0

	$SPM/spm_encode --model=$MDIR/spm/spm.model \
	--generate_vocabulary \
	< $DATADIR/train/train4spm.$TL \
	> $MDIR/spm/spm.vocab.$TL

	$SPM/spm_encode --model=$MDIR/spm/spm.model \
	--generate_vocabulary \
	< $DATADIR/train/train4spm.$SL \
	> $MDIR/spm/spm.vocab.$SL
}


# with vocab restriction https://github.com/google/sentencepiece#vocabulary-restriction
function seg_apply {
	spm_ini

	$SPM/spm_encode --model=$MDIR/spm/spm.model \
	--vocabulary=$MDIR/spm/spm.vocab.$TL --vocabulary_threshold=50 \
	< $DATADIR/train/train4spm.$TL \
	> $MDIR/spm/train.spm.$TL

	$SPM/spm_encode --model=$MDIR/spm/spm.model \
	--vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
	< $DATADIR/train/train4spm.$SL \
	> $MDIR/spm/train.spm.$SL

	$SPM/spm_encode --model=$MDIR/spm/spm.model \
	--vocabulary=$MDIR/spm/spm.vocab.$TL --vocabulary_threshold=50 \
	< $DATADIR/dev/dev4spm.$TL \
	> $MDIR/spm/dev.spm.$TL

	$SPM/spm_encode --model=$MDIR/spm/spm.model \
	--vocabulary=$MDIR/spm/spm.vocab.$SL --vocabulary_threshold=50 \
	< $DATADIR/dev/dev4spm.$SL \
	> $MDIR/spm/dev.spm.$SL

	marian_ini
	cat $MDIR/spm/train.spm.$SL $MDIR/spm/train.spm.$TL \
	| $MARIAN_VOCAB > $MDIR/spm/vocab.$SL$TL.yml
}


function seg_oov {
	for L in $SL $TL; do
		$MOSESSCRIPTS/analysis/oov.pl $MDIR/spm/dev.spm.$L < $MDIR/spm/train.spm.$L > $MDIR/oov-$L.log
	done
}

function train {
	marian_ini

	mkdir -p $MDIR/models

	$MARIAN_TRAIN \
        --model $MDIR/models/model.npz --type transformer \
        --train-sets $MDIR/spm/train.spm.$SL $MDIR/spm/train.spm.$TL \
        --max-length 700 \
        --vocabs $MDIR/spm/vocab.$SL$TL.yml $MDIR/spm/vocab.$SL$TL.yml \
        --mini-batch-fit -w $WORKSPACE --mini-batch 1000 --maxi-batch 1000 \
        --valid-freq 5000 --save-freq 5000 --disp-freq 500 \
        --valid-metrics bleu \
        --valid-sets $MDIR/spm/dev.spm.$SL $MDIR/spm/dev.spm.$TL \
        --valid-translation-output $MDIR/valid.spm.$SL.output --quiet-translation \
        --beam-size 6 --normalize=1.0 \
        --valid-mini-batch 64 \
        --early-stopping 10 --after-epochs $EPOCHS --cost-type=ce-mean-words \
	--log $MDIR/train.log --valid-log $MDIR/valid.log \
        --enc-depth 6 --dec-depth 6 \
        --transformer-heads 8 \
        --tied-embeddings-all \
        --transformer-dropout 0.1 --label-smoothing 0.1 \
        --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
        --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
        --devices $GPUS --sync-sgd --seed $SEED
}


if [ ! -f $MDIR/spm/spm.vocab.$SL ]; then
	seg_train
fi

if [ ! -f $MDIR/spm/vocab.$SL$TL.yml ]; then
	seg_apply
fi

if [ ! -f $MDIR/oov-$TL.log ]; then
	seg_oov
fi

train

