import spacy_udpipe
from tqdm import tqdm


def load_data(lang):
    data = []
    with open('data/TED2013.en-nl.' + lang, encoding="UTF-8") as f:
        lines = iter(f.readlines())
        line = next(lines, "<EOF>").rstrip()
        while line != "<EOF>":
            d = {}
            d['description'] = next(lines, "<EOF>").rstrip()
            d['cats'] = next(lines, "<EOF>").rstrip().split(",")
            d['id'] = int(next(lines, "<EOF>").rstrip())
            auth_title = next(lines, "<EOF>").rstrip().split(": ")
            if len(auth_title) == 1:
                d['author'] = None
                d['title'] = auth_title[0]
            else:
                d['author'] = auth_title[0]
                d['title'] = auth_title[1]
            d['sentences'] = []
            sent = next(lines, "<EOF>").rstrip()
            while sent[:4] != 'http' and sent != "<EOF>":
                d['sentences'].append(sent)
                sent = next(lines, "<EOF>").rstrip()
            data.append(d)
            line = sent
    return data


if __name__ == '__main__':

    langs = ["en", "nl"]

    for lang in langs:
        spacy_udpipe.download(lang)  # download English model

        data = load_data(lang)

        nlp = spacy_udpipe.load(lang)

        num_sentences = 0
        num_words = 0
        word_length = 0
        stop_words = 0
        pronouns = 0
        adjectives = 0
        nouns = 0

        for d in tqdm(data):
            num_sentences += len(d['sentences'])
            doc = nlp(d['sentences'])
            num_words += len(doc)
            for token in doc:
                if token.pos_ != "PUNCT":
                    word_length += len(token.text)
                if token.is_stop:
                    stop_words += 1
                if token.pos_ == "ADJ":
                    adjectives += 1
                elif token.pos_ == "PRON":
                    pronouns += 1
                elif token.pos_ == "NOUN":
                    nouns += 1

        word_length = word_length / num_words
        print("------------- %s -------------\n" % lang.upper())
        print("No. of documents:\t%i" % len(data))
        print("No. of sentences:\t%i" % (num_sentences))
        print("No. of tokens:\t\t%i" % (num_words))
        print("\n------------------------------\n")
        print("Average No. of sentences per document:\t %.2f" % (num_sentences / len(data)))
        print("Average No. of tokens per document:\t\t %.2f" % (num_words / len(data)))
        print("Average No. of tokens per sentence:\t\t %.2f" % (num_words / num_sentences))
        print("Average No. of characters per token:\t %.2f" % word_length)
        print("\n------------------------------\n")
        print("Average No. of stopwords per document:\t%.2f" % (stop_words / len(data)))
        print("Average No. of stopwords per sentence:\t%.2f" % (stop_words / num_sentences))
        print("\n------------------------------\n")
        print("Average No. of nouns per sentence:\t%.2f" % (nouns / num_sentences))
        print("Average No. of pronouns per sentence:\t%.2f" % (pronouns / num_sentences))
        print("Average No. of adjectives per sentence:\t%.2f" % (adjectives / num_sentences))
        print("\n------------------------------\n\n")
