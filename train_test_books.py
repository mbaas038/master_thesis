import os
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    BOOK_PATH = "/data/s3212262/thesis_data/Books"

    X = y = os.listdir(BOOK_PATH)

    os.mkdir(os.path.join(BOOK_PATH, "train"))
    os.mkdir(os.path.join(BOOK_PATH, "test"))

    # split train test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    for train in X_train:
        os.rename(os.path.join(BOOK_PATH, train), os.path.join(BOOK_PATH, "train", train))

    for test in X_test:
        os.rename(os.path.join(BOOK_PATH, test), os.path.join(BOOK_PATH, "test", test))
