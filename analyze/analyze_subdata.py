import spacy_udpipe
import time

if __name__ == '__main__':
    t0 = time.time()
    dir = "/data/s3212262/thesis_data/OpenSubtitles/raw/"
    ids = open(dir + "OpenSubtitles.en-nl.ids")
    en = open(dir + "OpenSubtitles.en-nl.en")
    nl = open(dir + "OpenSubtitles.en-nl.nl")

    spacy_udpipe.download("en")
    spacy_udpipe.download("nl")

    nlp_en = spacy_udpipe.load("en")
    nlp_nl = spacy_udpipe.load("nl")
    current_ids = []
    sentences_en = []
    sentences_nl = []
    num_documents = 0
    num_sentences = 0
    stats = {"en": {"num_words": 0,"word_length": 0,"stop_words": 0,"pronouns": 0,"adjectives": 0,"nouns": 0},
             "nl": {"num_words": 0,"word_length": 0,"stop_words": 0,"pronouns": 0,"adjectives": 0,"nouns": 0}}
    while True:
        print(sentences_en)
        ids_line = ids.readline()
        if ids_line is not None:
            ids_line = ids.readline().split()[:2]
        if ids_line != current_ids or not ids_line:
            if sentences_en and sentences_nl:
                doc_en = nlp_en(sentences_en)
                doc_nl = nlp_nl(sentences_nl)
                docs = {'en': doc_en, 'nl': doc_nl}
                for doc in docs:
                    stats[doc]['num_words'] += len(docs[doc])
                    for token in docs[doc]:
                        if token.pos_ != "PUNCT":
                            stats[doc]['word_length'] += len(token.text)
                        if token.is_stop:
                            stats[doc]['stop_words'] += 1
                        if token.pos_ == "ADJ":
                            stats[doc]['adjectives'] += 1
                        elif token.pos_ == "PRON":
                            stats[doc]['pronouns'] += 1
                        elif token.pos_ == "NOUN":
                            stats[doc]['nouns'] += 1
                sentences_en = []
                sentences_nl = []
            if ids_line is None:
                break
            else:
                current_ids = ids_line
                num_documents += 1
                if num_documents == 2:
                    break
        else:
            sentences_en.append(en.readline())
            sentences_nl.append(nl.readline())
        num_sentences += 1
    print(time.time() - t0)

    for lang in stats:
        print(stats)
        stats[lang]['word_length'] = stats[lang]['word_length'] / stats[lang]['num_words']
        print("------------- %s -------------\n" % lang.upper())
        print("No. of documents:\t%i" % num_documents)
        print("No. of sentences:\t%i" % (num_sentences))
        print("No. of tokens:\t\t%i" % (stats[lang]['num_words']))
        print("\n------------------------------\n")
        print("Average No. of sentences per document:\t %.2f" % (num_sentences / num_documents))
        print("Average No. of tokens per document:\t\t %.2f" % (stats[lang]['num_words'] / num_documents))
        print("Average No. of tokens per sentence:\t\t %.2f" % (stats[lang]['num_words'] / num_sentences))
        print("Average No. of characters per token:\t %.2f" % stats[lang]['word_length'])
        print("\n------------------------------\n")
        print("Average No. of stopwords per document:\t%.2f" % (stats[lang]['stop_words'] / num_documents))
        print("Average No. of stopwords per sentence:\t%.2f" % (stats[lang]['stop_words'] / num_sentences))
        print("\n------------------------------\n")
        print("Average No. of nouns per sentence:\t%.2f" % (stats[lang]['nouns'] / num_sentences))
        print("Average No. of pronouns per sentence:\t%.2f" % (stats[lang]['pronouns'] / num_sentences))
        print("Average No. of adjectives per sentence:\t%.2f" % (stats[lang]['adjectives'] / num_sentences))
        print("\n------------------------------\n\n")
