import os
import random

if __name__ == '__main__':
    random.seed(1001)
    DATA_DIR = "/data/s3212262/thesis_data/TED5/test"
    en_file = open(os.path.join(DATA_DIR, "test.it.en"), encoding="UTF-8").readlines()
    nl_file = open(os.path.join(DATA_DIR, "test.it.nl"), encoding="UTF-8").readlines()
    en_sample = open(os.path.join(DATA_DIR, "test.it.en.sample.clean"), encoding="UTF-8").readlines()
    nl_sample = open(os.path.join(DATA_DIR, "test.it.nl.sample.clean"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.it.en.sample.clean.final"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.it.nl.sample.clean.final"), "w", encoding="UTF-8")
    en_blocks = {}
    curr_en_blocks = {}
    en_block = []
    nl_blocks = {"hij": {}, "zij": {}, "het": {}}
    curr_nl_blocks = {"hij": {}, "zij": {}, "het": {}}
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

    for line in en_sample:
        if line == "\n":
            curr_en_blocks[en_block[0].split(":")[1].strip()] = en_block
            en_block = []
        else:
            en_block.append(line)

    for line in nl_sample:
        if line == "\n":
            curr_nl_blocks[nl_block[1].split(":")[1].strip()][nl_block[0].split(":")[1].strip()] = nl_block
            nl_block = []
        else:
            nl_block.append(line)

    unused_hij_block_ids = []
    for block_id in nl_blocks["hij"]:
        if block_id not in curr_nl_blocks["hij"].keys():
            unused_hij_block_ids.append(block_id)

    new_het_block_ids = random.sample(list(curr_nl_blocks["het"].keys()), 414)

    for block_id in curr_nl_blocks["hij"]:
        for l in curr_en_blocks[block_id]:
            out_en.write(l)
        out_en.write("\n")
        block = curr_nl_blocks["hij"][block_id]
        block = block[:-2] + [block[-1]]
        block[-1] = "T" + block[-1][2:]
        for l in block:
            out_nl.write(l)
        out_nl.write("\n")

    for block_id in new_het_block_ids:
        for l in curr_en_blocks[block_id]:
            out_en.write(l)
        out_en.write("\n")
        block = curr_nl_blocks["het"][block_id][:-1]
        for l in block:
            out_nl.write(l)
        out_nl.write("\n")

    for block_id in unused_hij_block_ids:
        for l in en_blocks[block_id]:
            out_en.write(l)
        out_en.write("\n")
        block = nl_blocks["hij"][block_id]
        block = block[:-2] + [block[-1]]
        block[-1] = "T" + block[-1][2:]
        for l in block:
            out_nl.write(l)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()
