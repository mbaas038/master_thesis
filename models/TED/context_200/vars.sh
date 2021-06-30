#!/bin/bash

# Common variables used in other scripts

MOSESSCRIPTS=$HOME/thesis/Software/mosesdecoder/scripts

MBD=/data/pg-wmt20/third/moses-scripts/generic/multi-bleu-detok.perl

MARIAN=$HOME/thesis/Software/marian/build
MARIAN_TRAIN=$MARIAN/marian
MARIAN_DECODER=$MARIAN/marian-decoder
MARIAN_VOCAB=$MARIAN/marian-vocab
MARIAN_SCORER=$MARIAN/marian-scorer

SPM=$HOME/thesis/Software/vcpkg/buildtrees/sentencepiece/x64-linux-dbg/src

WORKDIR=/data/s3212262/thesis_data/models/TED/context_200
TEDDIR=/data/s3212262/thesis_data/TED5
DATADIR=$TEDDIR/train_context_200
TESTDIR=$TEDDIR/test

function spm_ini {
	module purge
	module load git/2.23.0-GCCcore-8.3.0-nodocs
}

function marian_ini {
        module purge
        module load Boost/1.66.0-intel-2018a-Python-3.6.4
        module load CUDA/10.1.243-GCC-8.3.0 
}

