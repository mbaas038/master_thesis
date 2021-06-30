import os
import random

if __name__ == '__main__':
    # DATA_DIR = "./data/TED"
    random.seed(42)
    DATA_DIR = "/data/s3212262/thesis_data/Books/test"
    en_file = open(os.path.join(DATA_DIR, "test.you.en"), encoding="UTF-8").readlines()
    nl_file = open(os.path.join(DATA_DIR, "test.you.nl"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.you.en.sample"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.you.nl.sample"), "w", encoding="UTF-8")
    en_blocks = {}
    en_block = []
    nl_blocks = {"jij": {}, "je": {}, "jullie": {}, "u": {}}
    nl_block = []
    for line in en_file:
        if line == "\n":
            en_blocks[en_block[0].split(":")[1].strip()] = en_block
            en_block = []
        else:
            en_block.append(line)

    for line in nl_file:
        if line == "\n":
            nl_blocks[nl_block[1].split(":")[1].strip()][nl_block[0].split(":")[1].strip()] = nl_block
            nl_block = []
        else:
            nl_block.append(line)

    num_per_cat = 500 // len(nl_blocks)
    ids_per_cat = {pron: random.sample(list(nl_blocks[pron]), num_per_cat) for pron in nl_blocks}

    sample_en_blocks = []
    sample_nl_blocks = []
    for pron in ids_per_cat:
        for block_id in ids_per_cat[pron]:
            sample_en_blocks.append(en_blocks[block_id])
            sample_nl_blocks.append(nl_blocks[pron][block_id])

    assert len(sample_en_blocks) == len(sample_nl_blocks) and len(sample_en_blocks) == 500

    for i in range(len(sample_en_blocks)):
        for line in sample_en_blocks[i]:
            out_en.write(line)
        out_en.write("\n")

        for line in sample_nl_blocks[i]:
            out_nl.write(line)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()

    en_file = open(os.path.join(DATA_DIR, "test.it.en"), encoding="UTF-8").readlines()
    nl_file = open(os.path.join(DATA_DIR, "test.it.nl"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.it.en.sample"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.it.nl.sample"), "w", encoding="UTF-8")
    en_blocks = {}
    en_block = []
    nl_blocks = {"hij": {}, "het": {}}
    nl_block = []
    for line in en_file:
        if line == "\n":
            en_blocks[en_block[0].split(":")[1].strip()] = en_block
            en_block = []
        else:
            en_block.append(line)

    for line in nl_file:
        if line == "\n":
            nl_blocks[nl_block[1].split(":")[1].strip()][nl_block[0].split(":")[1].strip()] = nl_block
            nl_block = []
        else:
            nl_block.append(line)

    num_per_cat = 500 // len(nl_blocks)
    ids_per_cat = {pron: random.sample(list(nl_blocks[pron]), num_per_cat) for pron in nl_blocks}

    sample_en_blocks = []
    sample_nl_blocks = []
    for pron in ids_per_cat:
        for block_id in ids_per_cat[pron]:
            sample_en_blocks.append(en_blocks[block_id])
            sample_nl_blocks.append(nl_blocks[pron][block_id])

    assert len(sample_en_blocks) == len(sample_nl_blocks)

    for i in range(len(sample_en_blocks)):
        for line in sample_en_blocks[i]:
            out_en.write(line)
        out_en.write("\n")

        for line in sample_nl_blocks[i]:
            out_nl.write(line)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()
