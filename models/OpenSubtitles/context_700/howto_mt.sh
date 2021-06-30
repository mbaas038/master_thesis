#!/bin/bash

# Train literary-adapted MT EN->NL
# Based on EN->CA (enca_marian_spm, enca_mbart)

# CHANGELOG
# 20201230 Created



source `dirname "$0"`/vars.sh


#-----------------------------------------------------------------------------------------
function prepare4spm {
	I="$1"
	O="$2"

	cat "$I" |\
	    ${MOSESSCRIPTS}/tokenizer/normalize-punctuation.perl \
	    > $O
}


#-----------------------------------------------------------------------------------------
function model_sent {
#     TIME=6:00:00
#     ~/bin/rjob_v100.sh -p regular -m 64GB -t $TIME ./model_sent.sh 96000 1 10 27000


    TIME=3-00:00:00
    ~/bin/rjob_v100.sh -p gpu -t $TIME -m 16GB ./model_sent.sh 96000 1 10 27000

}

#-----------------------------------------------------------------------------------------
function decodes {
    TIME=00:20:00
    ~/bin/rjob_v100.sh -p gpushort -t $TIME ./decode.sh 6 1.0 8 27000
}

#-----------------------------------------------------------------------------------------
function scores {
  TIME=0:50:00
	~/bin/rjob_v100.sh -p gpushort -t $TIME ./contrastive.sh
}


#prepare4spm $DATADIR/train/train.en $DATADIR/train/train4spm.en
#prepare4spm $DATADIR/train/train.nl $DATADIR/train/train4spm.nl

#prepare4spm $DATADIR/dev/dev.en $DATADIR/dev/dev4spm.en
#prepare4spm $DATADIR/dev/dev.nl $DATADIR/dev/dev4spm.nl


#model_sent
decodes
#scores


