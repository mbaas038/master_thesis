import os
import random

if __name__ == '__main__':
    random.seed(1001)
    DATA_DIR = "/data/s3212262/thesis_data/OpenSubtitles5/test"
    en_file = open(os.path.join(DATA_DIR, "test.it.en"), encoding="UTF-8").readlines()
    nl_file = open(os.path.join(DATA_DIR, "test.it.nl"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.it.en.sample.clean.final"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.it.nl.sample.clean.final"), "w", encoding="UTF-8")
    en_blocks = {}
    en_block = []
    nl_blocks = {"hij": {}, "zij": {}, "het": {}}
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

    current_block_ids = []
    with open(os.path.join(DATA_DIR, "test.it.en.sample.clean"), encoding="utf-8") as curr:
        for line in curr.readlines():
            if line[:9] == "#BlockId:":
                current_block_ids.append(line.split(":")[1].strip())

    new_hij_blocks = []
    while len(new_hij_blocks) < 84:
        choice = random.choice(list(nl_blocks["hij"].keys()))
        if choice not in new_hij_blocks and choice not in current_block_ids:
            new_hij_blocks.append(choice)

    new_het_blocks = []
    while len(new_het_blocks) < 84:
        choice = random.choice(list(nl_blocks["het"].keys()))
        if choice not in new_het_blocks and choice not in current_block_ids:
            new_het_blocks.append(choice)

    out_en.write(open(os.path.join(DATA_DIR, "test.it.en.sample.clean"), encoding="utf-8").read())

    block = []
    for line in open(os.path.join(DATA_DIR, "test.it.nl.sample.clean"), encoding="utf-8").readlines():
        if line == "\n":
            pron = block[1].split(":")[1].strip()
            if pron == "hij":
                block = block[:-2] + [block[-1]]
                block[-1] = "T" + block[-1][2:]
            else:
                block = block[:-1]
            for l in block:
                out_nl.write(l)
            out_nl.write("\n")
            block = []
        else:
            block.append(line)

    for blockid in new_hij_blocks:
        for line in en_blocks[blockid]:
            out_en.write(line)
        out_en.write("\n")
        lines = nl_blocks["hij"][blockid][:-2] + [nl_blocks["hij"][blockid][-1]]
        lines[-1] = "T" + lines[-1][2:]
        for line in lines:
            out_nl.write(line)
        out_nl.write("\n")

    for blockid in new_het_blocks:
        for line in en_blocks[blockid]:
            out_en.write(line)
        out_en.write("\n")
        for line in nl_blocks["het"][blockid][:-1]:
            out_nl.write(line)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()
