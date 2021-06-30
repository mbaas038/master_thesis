import os
import sys


def blocks_to_context(en_blocks, nl_blocks, context_length=0, alts=0, delim="|"):
    prepped_sents_en, prepped_sents_nl = [], []
    for i in range(len(en_blocks)):
        block_en, block_nl, alt_sents = en_blocks[i], nl_blocks[i][:-alts], nl_blocks[i][-alts:]
        index = -1
        en_sents, nl_sents = [block_en[index] for _ in range(alts + 1)], [block_nl[index]] + alt_sents
        while True:
            index -= 1
            try:
                if len(block_en[index]) + 3 + len(en_sents[0]) > context_length or \
                        len(block_nl[index]) + 3 + len(nl_sents[0]) > context_length or -index == len(block_en):
                    prepped_sents_en += en_sents
                    prepped_sents_nl += nl_sents
                    index = -1
                    break
                for j in range(len(en_sents)):
                    en_sents[j] = block_en[index].rstrip() + " " + delim + " " + en_sents[j]
                    nl_sents[j] = block_nl[index].rstrip() + " " + delim + " " + nl_sents[j]
            except:
                print(index, len(block_en), block_nl)
                exit(-1)
    return prepped_sents_en, prepped_sents_nl


def lines_to_blocks(lines, alts=0):
    if alts:
        n = 25 + alts
        diff = 2
    else:
        n = 24
        diff = 1
    blocks = [[line.split(":", 1)[1].lstrip() for line in lines[i+diff:(i+n-2)]] for i in range(1, len(lines), n)]
    return blocks


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("ERROR: Context should be provided")
        exit(-1)

    CONTEXT_LENGTH = 0

    try:
        CONTEXT_LENGTH = int(sys.argv[1])
    except ValueError:
        print("Error: context length should be a valid integer (0 for baseline)")
        exit(-1)

    DATA_DIR = "/data/s3212262/thesis_data/OpenSubtitles5/test"

    IT_ALTS = 1
    YOU_ALTS = 3

    it_en = open(os.path.join(DATA_DIR, "test.it.en.sample.clean"), encoding="utf-8").readlines()
    it_nl = open(os.path.join(DATA_DIR, "test.it.nl.sample.clean"), encoding="utf-8").readlines()
    you_en = open(os.path.join(DATA_DIR, "test.you.en.sample.clean"), encoding="utf-8").readlines()
    you_nl = open(os.path.join(DATA_DIR, "test.you.nl.sample.clean"), encoding="utf-8").readlines()

    it_en_blocks = lines_to_blocks(it_en)
    it_nl_blocks = lines_to_blocks(it_nl, alts=IT_ALTS)
    you_en_blocks = lines_to_blocks(you_en)
    you_nl_blocks = lines_to_blocks(you_nl, alts=YOU_ALTS)

    out_sents_en_it, out_sents_nl_it = blocks_to_context(it_en_blocks, it_nl_blocks, context_length=CONTEXT_LENGTH, alts=IT_ALTS)
    out_sents_en_you, out_sents_nl_you = blocks_to_context(you_en_blocks, you_nl_blocks, context_length=CONTEXT_LENGTH, alts=YOU_ALTS)

    it_out_en = open(os.path.join(DATA_DIR, "test.it.%i.en") % CONTEXT_LENGTH, "w", encoding="utf-8")
    it_out_nl = open(os.path.join(DATA_DIR, "test.it.%i.nl") % CONTEXT_LENGTH, "w", encoding="utf-8")
    you_out_en = open(os.path.join(DATA_DIR, "test.you.%i.en") % CONTEXT_LENGTH, "w", encoding="utf-8")
    you_out_nl = open(os.path.join(DATA_DIR, "test.you.%i.nl") % CONTEXT_LENGTH, "w", encoding="utf-8")

    it_out_en_dec = open(os.path.join(DATA_DIR, "test.it.%i.dec.en") % CONTEXT_LENGTH, "w", encoding="utf-8")
    it_out_nl_dec = open(os.path.join(DATA_DIR, "test.it.%i.dec.nl") % CONTEXT_LENGTH, "w", encoding="utf-8")
    you_out_en_dec = open(os.path.join(DATA_DIR, "test.you.%i.dec.en") % CONTEXT_LENGTH, "w", encoding="utf-8")
    you_out_nl_dec = open(os.path.join(DATA_DIR, "test.you.%i.dec.nl") % CONTEXT_LENGTH, "w", encoding="utf-8")

    for i in range(len(out_sents_en_it)):
        it_out_en.write(out_sents_en_it[i])
        it_out_nl.write(out_sents_nl_it[i])

    for i in range(len(out_sents_en_you)):
        you_out_en.write(out_sents_en_you[i])
        you_out_nl.write(out_sents_nl_you[i])

    for i in range(0, len(out_sents_nl_it), IT_ALTS + 1):
        it_out_en_dec.write(out_sents_en_it[i])
        it_out_nl_dec.write(out_sents_nl_it[i])

    for i in range(0, len(out_sents_nl_you), YOU_ALTS + 1):
        you_out_en_dec.write(out_sents_en_you[i])
        you_out_nl_dec.write(out_sents_nl_you[i])

