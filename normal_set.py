import os
import sys


def extract_context(en_sents, nl_sents, context_length, delim="~"):
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
    # directory with train files
    TED_DIRS = ["/data/s3212262/thesis_data/TED5/test/71", "/data/s3212262/thesis_data/TED5/test/851"]
    SUB_DIRS = ["/data/s3212262/thesis_data/OpenSubtitles5/test/2013/2433956"]
    BOOKS_DIRS = ["/data/s3212262/thesis_data/Books/test/Tales of Beedle the Bard, The - J.K. Rowling"]
    out_ted = "/data/s3212262/thesis_data/TED5/test"
    out_sub = "/data/s3212262/thesis_data/OpenSubtitles5/test"
    out_book = "/data/s3212262/thesis_data/Books/test"
    # Create out directory for each out file
    for i in [0, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
        en_out = open(os.path.join(out_ted, f"normal.{i}.en"), "w", encoding="utf-8")
        nl_out = open(os.path.join(out_ted, f"normal.{i}.nl"), "w", encoding="utf-8")
        for ted_dir in TED_DIRS:
            en_sents = open(os.path.join(ted_dir, "en.raw"), encoding="utf-8").readlines()
            nl_sents = open(os.path.join(ted_dir, "nl.raw"), encoding="utf-8").readlines()

            context_sents_en, context_sents_nl = extract_context(en_sents, nl_sents, i)
            for sent in context_sents_en:
                en_out.write(sent + "\n")

            for sent in context_sents_nl:
                nl_out.write(sent + "\n")

        en_out.close()
        nl_out.close()

        en_out = open(os.path.join(out_book, f"normal.{i}.en"), "w", encoding="utf-8")
        nl_out = open(os.path.join(out_book, f"normal.{i}.nl"), "w", encoding="utf-8")
        for book_dir in BOOKS_DIRS:
            en_sents = open(os.path.join(book_dir, "en.raw"), encoding="utf-8").readlines()
            nl_sents = open(os.path.join(book_dir, "nl.raw"), encoding="utf-8").readlines()

            context_sents_en, context_sents_nl = extract_context(en_sents, nl_sents, i, delim="@@")
            for sent in context_sents_en:
                en_out.write(sent + "\n")

            for sent in context_sents_nl:
                nl_out.write(sent + "\n")

        en_out.close()
        nl_out.close()

    for i in [0, 200, 300, 400, 500, 600, 700, 800]:
        en_out = open(os.path.join(out_sub, f"normal.{i}.en"), "w", encoding="utf-8")
        nl_out = open(os.path.join(out_sub, f"normal.{i}.nl"), "w", encoding="utf-8")
        for sub_dir in SUB_DIRS:
            en_sents = open(os.path.join(sub_dir, "en.raw"), encoding="utf-8").readlines()
            nl_sents = open(os.path.join(sub_dir, "nl.raw"), encoding="utf-8").readlines()

            context_sents_en, context_sents_nl = extract_context(en_sents, nl_sents, i, delim="|")
            for sent in context_sents_en:
                en_out.write(sent + "\n")

            for sent in context_sents_nl:
                nl_out.write(sent + "\n")

        en_out.close()
        nl_out.close()


