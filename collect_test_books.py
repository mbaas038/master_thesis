
import os
from conllu import parse
from sacremoses import MosesDetokenizer


def parse_tags(file):
    tags = parse(open(file, encoding="UTF-8").read())
    return tags


def parse_align(en_align):
    en_align = en_align.split(" })")
    align_pairs = []
    for ind in range(1, len(en_align)):
        pair = en_align[ind].split("({")
        if len(pair) == 2:
            pair[0] = ind
            if pair[1]:
                pair[1] = [int(num) for num in pair[1].split()]
            else:
                pair[1] = [-1]
            align_pairs.append(pair)
    return align_pairs


def get_align(file):
    lines = open(file, encoding="UTF-8").readlines()
    align_pairs = [parse_align(lines[ind-1].rstrip())
                   for ind in range(1, len(lines)+1) if ind % 3 == 0]

    return align_pairs


def is_it(tag_info):
    if tag_info["feats"] is not None:
        try:
            return tag_info["lemma"] == "it" and \
                   tag_info["feats"]["Case"] == "Nom" and \
                   tag_info["feats"]["Gender"] == "Neut" and \
                   tag_info["feats"]["Number"] == "Sing" and \
                   tag_info["feats"]["Person"] == "3" and \
                   tag_info["feats"]["PronType"] == "Prs"
        except KeyError:
            return False
    return False


def is_hij_het(tag_info):
    if tag_info["feats"] is not None:
        try:
            return (tag_info["lemma"] == "hij" or tag_info["lemma"] == "het") and \
                    tag_info["feats"]["Person"] == "3" and \
                    tag_info["feats"]["PronType"] == "Prs" and \
                    tag_info["upos"] == "PRON"
        except KeyError:
            return False
    return False


def is_you(tag_info):
    if tag_info["feats"] is not None:
        try:
            return tag_info["lemma"] == "you" and \
                   tag_info["feats"]["Person"] == "2" and \
                   tag_info["feats"]["PronType"] == "Prs" and \
                   tag_info["feats"]["Case"] == "Nom" and \
                   tag_info["upos"] == "PRON"
        except KeyError:
            return False
    return False


def is_jij_je_jullie_u(tag_info):
    if tag_info["feats"] is not None:
        try:
            return (tag_info["lemma"] == "jij" or tag_info["lemma"] == "je" or
                    tag_info["lemma"] == "jullie" or tag_info["lemma"] == "u") and \
                    tag_info["feats"]["Person"] == "2" and \
                    tag_info["feats"]["PronType"] == "Prs" and \
                    tag_info["upos"] == "PRON"
        except KeyError:
            return False
    return False


def get_aligned_tag(tag_list, align_list, row, column):
    try:
        aligned = align_list[row][column]
    except IndexError:
        # if sentence longer than 100 tokens, aligner has included only the first 100 tokens. Not the most stylish way
        # to do this but since I don't want to use long sentences anyway, I'll leave it like this
        return False
    if len(aligned[1]) == 1 and aligned[1][0] != -1:
        token_id = aligned[1][0]
        nl_tag = tag_list[row].filter(id=token_id)
        if nl_tag:
            return nl_tag[0]
        return False


def create_alternatives(nl_sent, tag, alternatives):
    alt_translations = []
    tokens = nl_sent.rstrip().split()
    tok_id = tag["id"] - 1
    for alt in alternatives:
        if alt != tag["lemma"]:
            if tag["form"][0].isupper():
                alt = alt.capitalize()
            tokens[tok_id] = alt
            alt_translations.append(MD.detokenize(tokens)+"\n")
    return alt_translations


def is_valid_sentence(sent):
    if len(sent) > SENTENCE_LENGTH:
        return False
    punct = [".", "!", "?"]
    punct_cnt = 0
    for punc in punct:
        punct_cnt += sent.count(punc)
    if punct_cnt == 1:
        return True
    return False


def write_challenge_block(out_en, out_nl, en_sents, nl_sents, src, trg, alternatives, block_id):
    out_en.write("#BlockId: %i\n" % block_id)
    out_nl.write("#BlockId: %i\n" % block_id)
    out_en.write("#Src pronoun: %s\n" % src["lemma"])
    out_nl.write("#Trg pronoun: %s\n" % trg["lemma"])
    out_nl.write("#Antecedent Distance: \n")
    # write context
    context_len = len(en_sents) - 1
    for sent_i in range(context_len):
        out_en.write("S-%i: %s" % (context_len-sent_i, en_sents[sent_i]))
        out_nl.write("T-%i: %s" % (context_len-sent_i, nl_sents[sent_i]))
    # write sentence
    out_en.write("S: %s" % en_sents[-1])
    out_nl.write("T: %s" % nl_sents[-1])
    # write alts to nl file
    for alt_i, alt in enumerate(alternatives):
        out_nl.write("T%s: %s" % ("*"*(alt_i+1), alt))
    # trailing new line
    out_en.write("\n")
    out_nl.write("\n")


if __name__ == '__main__':

    TESTDIR = "/data/s3212262/thesis_data/Books/test"
    # TESTDIR = "./data/TED"
    CONTEXT_SENTS = 20
    SENTENCE_LENGTH = 100
    MD = MosesDetokenizer(lang="nl")

    testdirs = os.listdir(TESTDIR)
    you_block_num = 1
    it_block_num = 1
    it_out_en = open(os.path.join(TESTDIR, "test.it.en"), "w", encoding="utf-8")
    it_out_nl = open(os.path.join(TESTDIR, "test.it.nl"), "w", encoding="utf-8")
    you_out_en = open(os.path.join(TESTDIR, "test.you.en"), "w", encoding="utf-8")
    you_out_nl = open(os.path.join(TESTDIR, "test.you.nl"), "w", encoding="utf-8")
    for testdir in testdirs:
        en_raw = open(os.path.join(TESTDIR, testdir, "en.raw"), encoding="utf-8").readlines()
        nl_raw = open(os.path.join(TESTDIR, testdir, "nl.raw"), encoding="utf-8").readlines()
        en = open(os.path.join(TESTDIR, testdir, "en.tok"), encoding="utf-8").readlines()
        nl = open(os.path.join(TESTDIR, testdir, "nl.tok"), encoding="utf-8").readlines()
        en_tok = [line.rstrip().split() for line in en]
        nl_tok = [line.rstrip().split() for line in nl]
        en_tags = parse_tags(os.path.join(TESTDIR, testdir, "en.tag"))
        nl_tags = parse_tags(os.path.join(TESTDIR, testdir, "nl.tag"))
        align = get_align(os.path.join(TESTDIR, testdir, "en_nl.align"))

        for i in range(CONTEXT_SENTS, len(en_tok)):
            for j in range(len(en_tok[i])):

                en_token = en_tok[i][j]
                en_tag = en_tags[i][j]

                if is_it(en_tag):
                    aligned_tag = get_aligned_tag(nl_tags, align, i, j)
                    if aligned_tag and is_hij_het(aligned_tag) and is_valid_sentence(en_raw[i]):
                        alts = create_alternatives(nl[i], aligned_tag, ["hij", "het"])
                        en_block = en_raw[i - CONTEXT_SENTS:i + 1]
                        nl_block = nl_raw[i - CONTEXT_SENTS:i + 1]
                        write_challenge_block(it_out_en, it_out_nl, en_block, nl_block, en_tag, aligned_tag, alts, it_block_num)
                        it_block_num += 1
                        break

                elif is_you(en_tag):
                    aligned_tag = get_aligned_tag(nl_tags, align, i, j)
                    if aligned_tag and is_jij_je_jullie_u(aligned_tag) and is_valid_sentence(en_raw[i]):
                        alts = create_alternatives(nl[i], aligned_tag, ["jij", "je", "jullie", "u"])
                        en_block = en_raw[i-CONTEXT_SENTS:i+1]
                        nl_block = nl_raw[i-CONTEXT_SENTS:i+1]
                        write_challenge_block(you_out_en, you_out_nl, en_block, nl_block, en_tag, aligned_tag, alts, you_block_num)
                        you_block_num += 1
                        break

    it_out_en.close()
    it_out_nl.close()
    you_out_en.close()
    you_out_nl.close()

