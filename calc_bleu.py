import os
import sacrebleu
import sys

if __name__ == '__main__':
    for context_length in [0] + list(range(200, 1100, 100)):
        print(context_length)
        DATADIR = "normal/TED/pred"
        TRUEDIR = "normal/TED/true"
        ref_you = [[line.rstrip() for line in open(os.path.join(TRUEDIR, "normal.%i.nl" % context_length), encoding="UTF-8").readlines() if line.rstrip()]]

        sys_you = [line.rstrip() for line in open(os.path.join(DATADIR, "normal.pred.%i.nl" % context_length), encoding="UTF-8").readlines() if line.rstrip()]

        bleu = sacrebleu.corpus_bleu(sys_you, ref_you)
        print("BLEU: ", bleu.score)
