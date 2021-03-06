# master_thesis
This repository contains all code used during the experiments and writing of my master thesis Information Science at the University of Groningen.

## Reproduction steps

1. Download the data:
**TED**: [train/test](https://opus.nlpl.eu/TED2013.php) and [dev](https://wit3.fbk.eu/2017-01) data
**OpenSubtitles**: [data](https://opus.nlpl.eu/OpenSubtitles-v2018.php)
**Books**: unavailable :(
2. run `preprocess.sh` to create pos tags and word alignment files.
3. split large file into seperate documents with `split_files_ted.py` and `split_files_subs.py`.
4. Move Books vec files to directories with `books_vecs_to_dir.py`
5. Create pos tags and alignment for Books with `preprocess_books.sh`
6. Create train/dev/test split with `train_test_ted.py`, `train_test_subs.py` and `train_test_books.py`.
7. convert TED dev data from xml to txt with `dev_xml_to_txt.py`
8. create train file with `files_to_train_ted.py`, `files_to_train_subs.py` and `files_to_train_books.py`
9. create test suite with `collect_test_ted.py`, `collect_test_subs.py` and `collect_test_books.py`
10. Draw a random sample from the test suite with `random_test_sample_balanced.py`
11. Annotate data (this can be found in the data directory for TED and subtitles)
12. Convert test blocks to scoring format with `prep_for_contrastive.py`
13. run `howto_mt.sh` to train and evaluate models
14. collect evaluation results with `score_contrastive.py`
