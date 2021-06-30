import os
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    TED_PATH = "/data/s3212262/thesis_data/TED2"

    X = y = os.listdir(TED_PATH)

    os.mkdir(os.path.join(TED_PATH, "train"))
    os.mkdir(os.path.join(TED_PATH, "test"))

    # split train test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    for train in X_train:
        os.rename(os.path.join(TED_PATH, train), os.path.join(TED_PATH, "train", train))

    for test in X_test:
        os.rename(os.path.join(TED_PATH, test), os.path.join(TED_PATH, "test", test))

    # split train dev
    os.mkdir(os.path.join(TED_PATH, "dev"))

    train_path = os.path.join(TED_PATH, "train")

    X = y = os.listdir(train_path)

    X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.10, random_state=42)

    for dev in X_dev:
        os.rename(os.path.join(train_path, dev), os.path.join(TED_PATH, "dev", dev))
