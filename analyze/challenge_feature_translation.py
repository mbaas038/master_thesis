
from collections import defaultdict

if __name__ == '__main__':
    you_cnt = defaultdict(int)
    it_cnt = defaultdict(int)
    filename = '2020-12-07.154639.s3212262.A3.final'
    with open(filename, encoding="UTF-8") as f:
        index_line = f.readline()
        desc_line = False
        while index_line != '':
            target = f.readline().rstrip()
            source = f.readline().rstrip()
            if target[:4] == 'http':
                desc_line = True
                index_line = f.readline()
                continue

            # process line
            target = [tok.lower() for tok in target.split()]
            for term in source.split("})"):
                if term:
                    term = term.split("({")
                    term[0] = term[0].strip().lower()
                    indices = term[1].strip().split()

                    if term[0] == 'you':
                        if indices:
                            for i in indices:
                                you_cnt[target[int(i) - 1]] += 1
                        else:
                            you_cnt["<OMITTED>"] += 1

                    elif term[0] == 'it':
                        if indices:
                            for i in indices:
                                it_cnt[target[int(i) - 1]] += 1
                        else:
                            it_cnt["<OMITTED>"] += 1
            if desc_line:
                desc_line = False
                for i in range(6):
                    f.readline()

            index_line = f.readline()


    print("YOU:\n")

    total = sum(you_cnt.values())
    print("Total occurrences: %i" % total)
    print("Translations:")
    for translation, cnt in sorted(you_cnt.items(), key=lambda x: x[1], reverse=True):
        print("%s: %i (%.2f%%)" % (translation, cnt, (cnt / total * 100)))

    print("\nIT:\n")

    total = sum(it_cnt.values())
    print("Total occurrences: %i" % total)
    print("Translations:")
    for translation, cnt in sorted(it_cnt.items(), key=lambda x: x[1], reverse=True):
        print("%s: %i (%.2f%%)" % (translation, cnt, (cnt / total * 100)))