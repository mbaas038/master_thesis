import os
import sacrebleu
import sys

if __name__ == '__main__':
    for directory in ["OpenSubtitles", "Books", "TED/balanced", "TED/unbalanced"]:
        print(directory)
        it_trg = [line.rstrip() for line in open(os.path.join("data", directory, "test.it.0.nl"), encoding="utf-8").readlines()]

        ref, ref2 = [], []
        for i in range(len(it_trg)):
            if i % 2 == 0:
                ref.append(it_trg[i])
            else:
                ref2.append(it_trg[i])
        bleu = sacrebleu.corpus_bleu(ref, [ref2])
        print("it: ", bleu.score)

        you_trg = [line.rstrip() for line in
                  open(os.path.join("data", directory, "test.you.0.nl"), encoding="utf-8").readlines()]

        ref = []
        ref_alt = [[], [], []]
        for i in range(len(you_trg)):
            if i % 4 == 0:
                ref.append(you_trg[i])
            else:
                ref_alt[(i % 4) - 1].append(you_trg[i])
        total = 0
        for r in ref_alt:
            bleu = sacrebleu.corpus_bleu(ref, [r])
            total += bleu.score
        print("you:", total / len(ref_alt))

