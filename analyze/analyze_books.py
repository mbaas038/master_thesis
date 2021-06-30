import os
from conllu import parse

if __name__ == '__main__':
    BOOKDIR = "/data/s3212262/thesis_data/Books"

    num_docs = 0
    num_sents = 0
    num_tokens_en = 0
    num_tokens_nl = 0
    num_chars_en = 0
    num_chars_nl = 0
    num_prons_en = 0
    num_prons_nl = 0
    num_you = 0
    num_it = 0

    paths = [os.path.join(BOOKDIR, "train", d) for d in os.listdir(os.path.join(BOOKDIR, "train"))] + \
            [os.path.join(BOOKDIR, "dev", d) for d in os.listdir(os.path.join(BOOKDIR, "dev"))] + \
            [os.path.join(BOOKDIR, "test", d) for d in os.listdir(os.path.join(BOOKDIR, "test")) if os.path.isdir(os.path.join(BOOKDIR, "test", d))]

    for bookdir in paths:
        num_docs += 1
        path = os.path.join(BOOKDIR, "train", bookdir)
        en_file = open(os.path.join(path, "en.tok.clean"), encoding="utf-8").readlines()
        nl_file = open(os.path.join(path, "nl.tok.clean"), encoding="utf-8").readlines()
        en_tags = parse(open(os.path.join(path, "en.tag"), encoding="UTF-8").read())
        nl_tags = parse(open(os.path.join(path, "nl.tag"), encoding="UTF-8").read())

        for i in range(len(en_file)):
            num_sents += 1
            en_line = en_file[i].rstrip()
            nl_line = nl_file[i].rstrip()
            num_chars_en += len(en_line)
            num_chars_nl += len(nl_line)
            num_tokens_en += len(en_line.split())
            num_tokens_nl += len(nl_line.split())

            for tag in en_tags[i]:
                try:
                    if tag["upos"] == "PRON":
                        num_prons_en += 1
                        if tag["lemma"] == "you":
                            num_you += 1
                        elif tag["lemma"] == "it":
                            num_it += 1
                except KeyError:
                    continue

            for tag in nl_tags[i]:
                try:
                    if tag["upos"] == "PRON":
                        num_prons_nl += 1
                except KeyError:
                    continue

    print("Num docs", num_docs)
    print("Num sents", num_sents)
    print("Num tokens (en)", num_tokens_en)
    print("Num tokens (nl)", num_tokens_nl)
    print("Average sents per doc", num_sents / num_docs)
    print("Average tokens per doc (en)", num_tokens_en / num_docs)
    print("Average tokens per doc (nl)", num_tokens_nl / num_docs)
    print("Average tokens per sentence (en)", num_tokens_en / num_sents)
    print("Average tokens per sentence (nl)", num_tokens_nl / num_sents)
    print("Average chars per token (en)", num_chars_en / num_tokens_en)
    print("Average chars per token (nl)", num_chars_nl / num_tokens_nl)
    print("Average prons per sent (en)", num_prons_en / num_sents)
    print("Average prons per sent (nl)", num_prons_nl / num_sents)
    print("It per 1000 tokens", num_it / num_tokens_en * 1000)
    print("You per 1000 tokens", num_you / num_tokens_en * 1000)

