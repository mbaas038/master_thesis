import os
import random
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    SUB_PATH = "/data/s3212262/thesis_data/OpenSubtitles5"

    X = y = [(year, doc) for year in os.listdir(SUB_PATH) for doc in os.listdir(os.path.join(SUB_PATH, year))]

    os.mkdir(os.path.join(SUB_PATH, "train"))
    os.mkdir(os.path.join(SUB_PATH, "test"))

    # split train test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    for year, doc in X_train:
        train_year_dir = os.path.join(SUB_PATH, "train", year)
        if not os.path.isdir(train_year_dir):
            os.mkdir(train_year_dir)
        os.rename(os.path.join(SUB_PATH, year, doc), os.path.join(train_year_dir, doc))

    for year, doc in X_test:
        test_year_dir = os.path.join(SUB_PATH, "test", year)
        if not os.path.isdir(test_year_dir):
            os.mkdir(test_year_dir)
        os.rename(os.path.join(SUB_PATH, year, doc), os.path.join(test_year_dir, doc))

    # split train dev
    os.mkdir(os.path.join(SUB_PATH, "dev"))

    train_path = os.path.join(SUB_PATH, "train")

    X = y = [(year, doc) for year in os.listdir(train_path) for doc in os.listdir(os.path.join(train_path, year))]

    # X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.10, random_state=42)
    random.seed(42)
    X_dev = random.sample(X, k=3)
    for year, doc in X_dev:
        dev_year_dir = os.path.join(SUB_PATH, "dev", year)
        if not os.path.isdir(dev_year_dir):
            os.mkdir(dev_year_dir)
        os.rename(os.path.join(train_path, year, doc), os.path.join(dev_year_dir, doc))
