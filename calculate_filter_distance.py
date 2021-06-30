
import os

if __name__ == '__main__':
    BOOKS_DIR = "/data/s3212262/thesis_data/Books/train_books"
    filter_indexes = []
    for filename in os.listdir(BOOKS_DIR):
        book = open(os.path.join(BOOKS_DIR, filename), encoding="utf-8").readlines()
        indexes = []
        for i in range(len(book)):
            line = book[i]
            distance = float(line.rstrip().split("\t")[-1])
            if distance > 0.7:
                indexes.append(i)
        filter_indexes.append(indexes)

    total = 0
    for book in filter_indexes:
        for i in range(1, len(book)):
            total += book[i] - book[i-1]

    print("Average distance between filtered length", total / sum([len(l) for l in filter_indexes]))

