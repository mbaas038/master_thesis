
import os

if __name__ == '__main__':

    TED_DIR = "/data/s3212262/thesis_data/TED"
    OUT_DIR = "/data/s3212262/thesis_data/TED4"

    EN_FILE = os.path.join(TED_DIR, "TED2013.en-nl.en")
    NL_FILE = os.path.join(TED_DIR, "TED2013.en-nl.nl")
    EN_FILE_TOK = os.path.join(TED_DIR, "TED2013.en-nl.tok.en")
    NL_FILE_TOK = os.path.join(TED_DIR, "TED2013.en-nl.tok.nl")
    EN_FILE_TAG = os.path.join(TED_DIR, "TED2013.en-nl.tag.en")
    NL_FILE_TAG = os.path.join(TED_DIR, "TED2013.en-nl.tag.nl")
    ALIGN_FILE = os.path.join(TED_DIR, "giza_out", "2020-12-07.154639.s3212262.A3.final")

    raw_en = open(EN_FILE, encoding="utf-8")
    raw_nl = open(NL_FILE, encoding="utf-8")
    tok_en = open(EN_FILE_TOK, encoding="utf-8")
    tok_nl = open(NL_FILE_TOK, encoding="utf-8")
    tag_en = open(EN_FILE_TAG, encoding="utf-8")
    tag_nl = open(NL_FILE_TAG, encoding="utf-8")
    align = open(ALIGN_FILE, encoding="utf-8")

    # skip index lines
    for i in range(2):
        tag_en.readline()
        tag_nl.readline()

    en_doc = None
    nl_doc = None
    en_doc_tok = None
    nl_doc_tok = None
    en_tag_doc = None
    nl_tag_doc = None
    align_doc = None

    en_line = raw_en.readline()
    nl_line = raw_nl.readline()
    en_line_tok = tok_en.readline()
    nl_line_tok = tok_nl.readline()

    while en_line:
        if en_line[0:18] == "http://www.ted.com":
            if en_doc is not None and nl_doc is not None:
                en_doc.close()
                nl_doc.close()
                en_doc_tok.close()
                nl_doc_tok.close()
                en_tag_doc.close()
                nl_tag_doc.close()
                align_doc.close()

            # skip meta-lines
            dir_id = 0
            for i in range(5):
                # raw files
                en_line = raw_en.readline()
                nl_line = raw_nl.readline()

                # tok files
                if i == 2:
                    # use doc id as directory name
                    dir_id = tok_en.readline().rstrip()
                else:
                    en_line_tok = tok_en.readline()
                nl_line_tok = tok_nl.readline()

                # tag files
                line = tag_en.readline().rstrip()
                while line:
                    line = tag_en.readline().rstrip()

                line = tag_nl.readline().rstrip()
                while line:
                    line = tag_nl.readline().rstrip()

                # align files
                for _ in range(3):
                    align.readline()

            # create new directory
            path = os.path.join(OUT_DIR, dir_id)
            os.mkdir(path)

            # create new files
            en_doc = open(os.path.join(path, "en.raw"), "w", encoding="utf-8")
            nl_doc = open(os.path.join(path, "nl.raw"), "w", encoding="utf-8")
            en_doc_tok = open(os.path.join(path, "en.tok"), "w", encoding="utf-8")
            nl_doc_tok = open(os.path.join(path, "nl.tok"), "w", encoding="utf-8")
            en_tag_doc = open(os.path.join(path, "en.tag"), "w", encoding="utf-8")
            nl_tag_doc = open(os.path.join(path, "nl.tag"), "w", encoding="utf-8")
            align_doc = open(os.path.join(path, "en-nl.align"), "w", encoding="utf-8")

        # write to plain text files
        en_doc.write(en_line)
        nl_doc.write(nl_line)

        en_line = raw_en.readline()
        nl_line = raw_nl.readline()

        # write to tok files
        en_doc_tok.write(en_line_tok)
        nl_doc_tok.write(nl_line_tok)

        en_line_tok = tok_en.readline()
        nl_line_tok = tok_nl.readline()

        # write to tag files
        line = tag_en.readline().rstrip()
        while line:
            en_tag_doc.write(line + "\n")
            line = tag_en.readline().rstrip()
        en_tag_doc.write("\n")

        line = tag_nl.readline().rstrip()
        while line:
            nl_tag_doc.write(line + "\n")
            line = tag_nl.readline().rstrip()
        nl_tag_doc.write("\n")

        # write to align file
        for i in range(3):
            align_doc.write(align.readline())
