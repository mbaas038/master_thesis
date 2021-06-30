import os

if __name__ == '__main__':
    BOOKS_DIR = "/data/s3212262/thesis_data/Books/train_books"
    for filename in os.listdir(BOOKS_DIR):

        # create dir
        book_dir = os.path.join(BOOKS_DIR, filename.split(".tok.norm")[0])
        os.mkdir(book_dir)

        # create out files
        out_en = open(os.path.join(book_dir, "en.tok"), "w", encoding="utf-8")
        out_nl = open(os.path.join(book_dir, "nl.tok"), "w", encoding="utf-8")
        out_en_no_delim = open(os.path.join(book_dir, "en.tok.no_delim"), "w", encoding="utf-8")
        out_nl_no_delim = open(os.path.join(book_dir, "nl.tok.no_delim"), "w", encoding="utf-8")

        book = open(os.path.join(BOOKS_DIR, filename), encoding="utf-8").readlines()
        for line in book:
            fields = line.rstrip().split("\t")
            distance = float(fields[2])
            if distance < 0.7:
                out_en.write(fields[0] + "\n")
                out_nl.write(fields[1] + "\n")
                out_en_no_delim.write(fields[0].replace("~~~ ", "") + "\n")
                out_nl_no_delim.write(fields[1].replace("~~~ ", "") + "\n")

        out_en.close()
        out_nl.close()
        out_en_no_delim.close()
        out_nl_no_delim.close()


