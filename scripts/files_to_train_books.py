import os
import sys


def extract_context(en_sents, nl_sents, context_length, delim="@@"):
    # baseline
    if not context_length:
        return [line.rstrip() for line in en_sents], [line.rstrip() for line in nl_sents]
    # do something with more context
    current_line_en = ""
    en_train = []
    current_line_nl = ""
    nl_train = []
    for i in range(len(en_sents)):
        en_line, nl_line = en_sents[i].rstrip(), nl_sents[i].rstrip()
        if len(en_line) + len(current_line_en) <= context_length and len(nl_line) + len(current_line_nl) <= context_length:
            if current_line_en:
                current_line_en += " " + delim + " "
                current_line_nl += " " + delim + " "
            current_line_en += en_line
            current_line_nl += nl_line
        else:
            en_train.append(current_line_en)
            nl_train.append(current_line_nl)
            if len(en_line) <= context_length and len(nl_line) <= context_length:
                current_line_en = en_line
                current_line_nl = nl_line
            else:
                current_line_en = ""
                current_line_nl = ""
    if current_line_en:
        en_train.append(current_line_en)
        nl_train.append(current_line_nl)
    return en_train, nl_train


if __name__ == '__main__':

    # check if context length is specified
    if len(sys.argv) != 2:
        print("Error: context length not specified")
        exit(-1)

    CONTEXT_LENGTH = 0

    try:
        CONTEXT_LENGTH = int(sys.argv[1])
    except ValueError:
        print("Error: context length should be a valid integer (0 for baseline)")
        exit(-1)

    # directory with train files
    BOOK_DIR = "/data/s3212262/thesis_data/Books"
    TRAIN_DIR = os.path.join(BOOK_DIR, "train")
    DEV_DIR = os.path.join(BOOK_DIR, "dev")

    # Create out directory for each out file
    out_dir = os.path.join(BOOK_DIR, "train_context_%i" % CONTEXT_LENGTH)
    out_train = os.path.join(out_dir, "train")
    out_dev = os.path.join(out_dir, "dev")
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        os.mkdir(out_train)
        os.mkdir(out_dev)

    en_out = open(os.path.join(out_train, "train.en"), "w", encoding="utf-8")
    nl_out = open(os.path.join(out_train, "train.nl"), "w", encoding="utf-8")

    # extract subdirectories containing file per directory
    file_dirs = os.listdir(TRAIN_DIR)

    for file_dir in file_dirs:
        en_sents = open(os.path.join(TRAIN_DIR, file_dir, "en.raw"), encoding="utf-8").readlines()
        nl_sents = open(os.path.join(TRAIN_DIR, file_dir, "nl.raw"), encoding="utf-8").readlines()

        context_sents_en, context_sents_nl = extract_context(en_sents, nl_sents, CONTEXT_LENGTH)
        for sent in context_sents_en:
            en_out.write(sent + "\n")

        for sent in context_sents_nl:
            nl_out.write(sent + "\n")

    en_out.close()
    nl_out.close()

    en_out = open(os.path.join(out_dev, "dev.en"), "w", encoding="utf-8")
    nl_out = open(os.path.join(out_dev, "dev.nl"), "w", encoding="utf-8")

    # extract subdirectories containing file per directory
    file_dirs = os.listdir(DEV_DIR)

    for file_dir in file_dirs:
        en_sents = open(os.path.join(DEV_DIR, file_dir, "en.raw"), encoding="utf-8").readlines()
        nl_sents = open(os.path.join(DEV_DIR, file_dir, "nl.raw"), encoding="utf-8").readlines()

        context_sents_en, context_sents_nl = extract_context(en_sents, nl_sents, CONTEXT_LENGTH)
        for sent in context_sents_en:
            en_out.write(sent + "\n")

        for sent in context_sents_nl:
            nl_out.write(sent + "\n")

    en_out.close()
    nl_out.close()
