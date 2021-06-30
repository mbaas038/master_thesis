
import os

if __name__ == '__main__':

    SUB_DIR = "/data/s3212262/thesis_data/OpenSubtitles"
    OUT_DIR = "/data/s3212262/thesis_data/OpenSubtitles4"

    EN_FILE_RAW = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.en")
    NL_FILE_RAW = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.nl")
    EN_FILE = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.tok.en")
    NL_FILE = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.tok.nl")
    IDS_FILE = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.ids")
    EN_FILE_TAG = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.tag.en")
    NL_FILE_TAG = os.path.join(SUB_DIR, "raw", "OpenSubtitles.en-nl.tag.nl")
    ALIGN_FILE = os.path.join(SUB_DIR, "raw", "giza_out", "2021-01-07.095059.s3212262.A3.final")

    raw_en = open(EN_FILE_RAW, encoding="utf-8")
    raw_nl = open(NL_FILE_RAW, encoding="utf-8")
    tok_en = open(EN_FILE, encoding="utf-8")
    tok_nl = open(NL_FILE, encoding="utf-8")
    ids = open(IDS_FILE, encoding="utf-8")
    tag_en = open(EN_FILE_TAG, encoding="utf-8")
    tag_nl = open(NL_FILE_TAG, encoding="utf-8")
    align = open(ALIGN_FILE, encoding="utf-8")

    # skip index lines
    for i in range(2):
        tag_en.readline()
        tag_nl.readline()

    current_file_pair = []
    en_doc = None
    nl_doc = None
    en_doc_tok = None
    nl_doc_tok = None
    en_tag_doc = None
    nl_tag_doc = None
    align_doc = None
    ids_line = ids.readline()
    en_line = raw_en.readline()
    nl_line = raw_nl.readline()
    en_tok_line = tok_en.readline()
    nl_tok_line = tok_nl.readline()
    while ids_line:
        file_pair = ids_line.split()[:2]
        if file_pair != current_file_pair:
            current_file_pair = file_pair
            if en_doc is not None and nl_doc is not None:
                en_doc.close()
                nl_doc.close()
                en_doc_tok.close()
                nl_doc_tok.close()
                en_tag_doc.close()
                nl_tag_doc.close()
                align_doc.close()

            # create new directory
            directory = file_pair[0].split("/")[1:3]
            if not os.path.exists(os.path.join(OUT_DIR, directory[0])):
                os.mkdir(os.path.join(OUT_DIR, directory[0]))
            path = os.path.join(OUT_DIR, directory[0], directory[1])
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

        # write to tok files
        en_doc_tok.write(en_tok_line)
        nl_doc_tok.write(nl_tok_line)

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

        ids_line = ids.readline()
        en_line = raw_en.readline()
        nl_line = raw_nl.readline()
        en_tok_line = tok_en.readline()
        nl_tok_line = tok_nl.readline()
