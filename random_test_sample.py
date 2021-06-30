import os
import random

if __name__ == '__main__':
    # DATA_DIR = "./data/TED"
    random.seed(42)
    DATA_DIR = "/data/s3212262/thesis_data/TED5/test"
    en_file = open(os.path.join(DATA_DIR, "test.you.en"), encoding="UTF-8").readlines()
    nl_file = open(os.path.join(DATA_DIR, "test.you.nl"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.you.en.sample"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.you.nl.sample"), "w", encoding="UTF-8")
    en_blocks = []
    en_block = []
    nl_blocks = []
    nl_block = []
    for line in en_file:
        if line == "\n":
            en_blocks.append(en_block)
            en_block = []
        else:
            en_block.append(line)

    for line in nl_file:
        if line == "\n":
            nl_blocks.append(nl_block)
            nl_block = []
        else:
            nl_block.append(line)

    assert len(nl_blocks) == len(en_blocks)

    ids = random.sample(range(len(en_blocks)), 500)
    for i in ids:
        for line in en_blocks[i]:
            out_en.write(line)
        out_en.write("\n")

        for line in nl_blocks[i]:
            out_nl.write(line)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()

    en_file = open(os.path.join(DATA_DIR, "test.it.en"), encoding="UTF-8").readlines()
    nl_file = open(os.path.join(DATA_DIR, "test.it.nl"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.it.en.sample"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.it.nl.sample"), "w", encoding="UTF-8")
    en_blocks = []
    en_block = []
    nl_blocks = []
    nl_block = []
    for line in en_file:
        if line == "\n":
            en_blocks.append(en_block)
            en_block = []
        else:
            en_block.append(line)

    for line in nl_file:
        if line == "\n":
            nl_blocks.append(nl_block)
            nl_block = []
        else:
            nl_block.append(line)

    assert len(nl_blocks) == len(en_blocks)

    ids = random.sample(range(len(en_blocks)), 500)
    for i in ids:
        for line in en_blocks[i]:
            out_en.write(line)
        out_en.write("\n")

        for line in nl_blocks[i]:
            out_nl.write(line)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()
