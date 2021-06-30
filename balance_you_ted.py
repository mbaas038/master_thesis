import os
import random


def file_to_blocks(en, nl):
    en_blocks = {}
    en_block = []
    nl_blocks = {"jij": {}, "je": {}, "jullie": {}, "u": {}}
    nl_block = []
    for line in en:
        if line == "\n":
            en_blocks[en_block[0].split(":")[1].strip()] = en_block
            en_block = []
        else:
            en_block.append(line)

    for line in nl:
        if line == "\n":
            nl_blocks[nl_block[1].split(":")[1].strip()][nl_block[0].split(":")[1].strip()] = nl_block
            nl_block = []
        else:
            nl_block.append(line)

    return en_blocks, nl_blocks

if __name__ == '__main__':
    DATA_DIR = "/data/s3212262/thesis_data/TED5/test"
    #DATA_DIR = "data/TED"

    selected_you_en = open(os.path.join(DATA_DIR, "test.you.en.sample.clean"), encoding="UTF-8").readlines()
    selected_you_nl = open(os.path.join(DATA_DIR, "test.you.nl.sample.clean"), encoding="UTF-8").readlines()
    out_en = open(os.path.join(DATA_DIR, "test.you.en.sample.clean.final"), "w", encoding="UTF-8")
    out_nl = open(os.path.join(DATA_DIR, "test.you.nl.sample.clean.final"), "w", encoding="UTF-8")
    en_blocks, nl_blocks = file_to_blocks(selected_you_en, selected_you_nl)

    all_you_en = open(os.path.join(DATA_DIR, "test.you.en"), encoding="UTF-8").readlines()
    all_you_nl = open(os.path.join(DATA_DIR, "test.you.nl"), encoding="UTF-8").readlines()
    all_en_blocks, all_nl_blocks = file_to_blocks(all_you_en, all_you_nl)

    jij_options = set(all_nl_blocks["jij"].keys()) - set(nl_blocks["jij"].keys())
    jullie_options = set(all_nl_blocks["jullie"].keys()) - set(nl_blocks["jullie"].keys())
    u_options = set(all_nl_blocks["u"].keys()) - set(nl_blocks["u"].keys())

    for pron in ["jij", "jullie", "u"]:
        for blockid in nl_blocks[pron]:
            for line in en_blocks[blockid]:
                out_en.write(line)
            out_en.write("\n")
            for line in nl_blocks[pron][blockid]:
                out_nl.write(line)
            out_nl.write("\n")

    je_ids = random.sample(nl_blocks["je"].keys(), 210)
    for blockid in je_ids:
        for line in en_blocks[blockid]:
            out_en.write(line)
        out_en.write("\n")
        for line in nl_blocks["je"][blockid]:
            out_nl.write(line)
        out_nl.write("\n")

    for blockid in jij_options:
        for line in all_en_blocks[blockid]:
            out_en.write(line)
        out_en.write("\n")
        for line in all_nl_blocks["jij"][blockid]:
            out_nl.write(line)
        out_nl.write("\n")

    for blockid in jullie_options:
        for line in all_en_blocks[blockid]:
            out_en.write(line)
        out_en.write("\n")
        for line in all_nl_blocks["jullie"][blockid]:
            out_nl.write(line)
        out_nl.write("\n")

    for blockid in u_options:
        for line in all_en_blocks[blockid]:
            out_en.write(line)
        out_en.write("\n")
        for line in all_nl_blocks["u"][blockid]:
            out_nl.write(line)
        out_nl.write("\n")

    out_en.close()
    out_nl.close()



