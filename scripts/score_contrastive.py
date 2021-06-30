
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def get_results(data_type, context_length):
    IT_OPTIONS = ["hij", "het"]
    YOU_OPTIONS = ["jij", "je", "jullie", "u"]

    CONTEXT_LINES = 0
    if data_type == "TED/balanced" or data_type == "TED/unbalanced":
        CONTEXT_LINES = 14
    elif data_type == "OpenSubtitles":
        CONTEXT_LINES = 39
    elif data_type == "Books":
        CONTEXT_LINES = 24
    else:
        print("data_type should be TED/balanced, TED/unbalanced, OpenSubtitles or Books")
        return

    FILE_PREFIX = ""
    if data_type == "TED/unbalanced":
        FILE_PREFIX = "unb."

    if context_length == "0":
        context_length = "baseline"
    else:
        context_length = "context_" + context_length

    print(data_type, context_length)

    # Predictions
    it_scores = open(os.path.join("data", data_type, context_length, "scores", FILE_PREFIX + "test.it.scores"),
                     encoding="utf-8").readlines()
    you_scores = open(os.path.join("data", data_type, context_length, "scores", FILE_PREFIX + "test.you.scores"),
                      encoding="utf-8").readlines()

    it_blocks = [[float(score.rstrip()) for score in it_scores[i:i + len(IT_OPTIONS)]]
                 for i in range(0, len(it_scores), len(IT_OPTIONS))]
    you_blocks = [[float(score.rstrip()) for score in you_scores[i:i + len(YOU_OPTIONS)]]
                  for i in range(0, len(you_scores), len(YOU_OPTIONS))]

    # True labels
    it_lines = open(os.path.join("data", data_type, "score_true", "test.it.nl.sample.clean"), encoding="utf-8").readlines()
    you_lines = open(os.path.join("data", data_type, "score_true", "test.you.nl.sample.clean"), encoding="utf-8").readlines()

    it_true = [IT_OPTIONS.index(it_lines[i].rstrip().split(":")[1].lstrip()) for i in
               range(1, len(it_lines), CONTEXT_LINES + len(IT_OPTIONS))]
    you_true = [YOU_OPTIONS.index(you_lines[i].rstrip().split(":")[1].lstrip()) for i in
                range(1, len(you_lines), CONTEXT_LINES + len(YOU_OPTIONS))]

    it_pred = []
    for i in range(len(it_blocks)):
        block = it_blocks[i]
        true = it_true[i]
        pred_dict = {true: block[0]}
        for j in range(1, len(IT_OPTIONS)):
            for k in range(j - 1, len(IT_OPTIONS)):
                if k != true and k not in pred_dict:
                    pred_dict[k] = block[j]
                    break
        pred_dict['pred'] = max(pred_dict, key=pred_dict.get)
        pred_dict["true"] = true
        it_pred.append(pred_dict)

    you_pred = []
    for i in range(len(you_blocks)):
        block = you_blocks[i]
        true = you_true[i]
        pred_dict = {true: block[0]}
        for j in range(1, len(YOU_OPTIONS)):
            for k in range(j - 1, len(YOU_OPTIONS)):
                if k != true and k not in pred_dict:
                    pred_dict[k] = block[j]
                    break
        pred_dict['pred'] = max(pred_dict, key=pred_dict.get)
        pred_dict["true"] = true
        you_pred.append(pred_dict)

    # it
    print("-------------------------------\nit\n-------------------------------")

    it_predictions = [d["pred"] for d in it_pred]
    if data_type == "TED/balanced":
        it_predictions = it_predictions[:27] + it_predictions[47:]
        it_true = it_true[:27] + it_true[47:]
    # accuracy
    it_acc = accuracy_score(it_true, it_predictions)
    print("Accuracy: %.2f\n" % it_acc)

    # Classification Report
    it_cr = classification_report(it_true, it_predictions, labels=[0, 1], target_names=IT_OPTIONS, zero_division=0, output_dict=True)
    # print(it_cr["macro avg"]["precision"])

    # Confusion Matrix
    it_cm = pd.DataFrame(confusion_matrix(it_true, it_predictions, labels=[0, 1]), columns=IT_OPTIONS, index=IT_OPTIONS)
    print(it_cm)

    # certainty & severity
    certainties = []
    severities = []
    for prediction in it_pred:
        if prediction["true"] == prediction["pred"]:
            certainty = 0.0
            for i in range(len(IT_OPTIONS)):
                if i != prediction["true"]:
                    certainty += abs(prediction[prediction["true"]] - prediction[i])
            certainty /= (len(IT_OPTIONS) - 1)
            certainties.append(certainty)
        else:
            severity = abs(prediction[prediction["true"]] - prediction[prediction["pred"]])
            severities.append(severity)
    it_certainty = sum(certainties) / len(certainties)
    it_severity = sum(severities) / len(severities)
    print("\nAverage certainty: %.2f" % it_certainty)
    print("Average error severity: %.2f" % it_severity)

    print()

    # you
    print("-------------------------------\nyou\n-------------------------------")

    you_predictions = [d["pred"] for d in you_pred]
    # accuracy
    you_acc = accuracy_score(you_true, you_predictions)
    print("Accuracy: %.2f\n" % you_acc)

    # classification report
    you_cr = classification_report(you_true, you_predictions, labels=[0, 1, 2, 3], target_names=YOU_OPTIONS,
                                   zero_division=0, output_dict=True)
    # print(you_cr)

    # confusion matrix
    you_cm = pd.DataFrame(confusion_matrix(you_true, you_predictions, labels=[0, 1, 2, 3]), columns=YOU_OPTIONS,
                          index=YOU_OPTIONS)
    print(you_cm)
    # certainty & severity
    certainties = []
    severities = []
    for prediction in you_pred:
        if prediction["true"] == prediction["pred"]:
            certainty = 0.0
            for i in range(len(YOU_OPTIONS)):
                if i != prediction["true"]:
                    certainty += abs(prediction[prediction["true"]] - prediction[i])
            certainty /= (len(YOU_OPTIONS) - 1)
            certainties.append(certainty)
        else:
            severity = abs(prediction[prediction["true"]] - prediction[prediction["pred"]])
            severities.append(severity)

    you_certainty = sum(certainties) / len(certainties)
    you_severity = sum(severities) / len(severities)
    print("\nAverage certainty: %.2f" % you_certainty)
    print("Average error severity: %.2f" % you_severity)

    print()

    return {
        "it": {"acc": it_acc, "sev": it_severity, "cert": it_certainty, "cr": it_cr},
        "you": {"acc": you_acc, "sev": you_severity, "cert": you_certainty, "cr": you_cr}
    }


def plot_acc(it_acc, you_acc):
    labels = ["baseline"] + [str(i) for i in range(200, (len(it_acc) + 1) * 100, 100)]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 5))
    rects1 = ax.bar(x - width / 2, it_acc, width, label='It')
    rects2 = ax.bar(x + width / 2, you_acc, width, label='You')

    ax.set_ylabel('Accuracy')
    title = sys.argv[1].replace("/", " (").replace("unbalanced", "original") + ")" if sys.argv[1][:3] == "TED" else sys.argv[1]
    ax.set_title(f'Accuracy for {title}')
    ax.set_ylim([0.4, 1.1])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    for rect, label in zip(rects1, [f"{it:.2f}" for it in it_acc]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    for rect, label in zip(rects2, [f"{you:.2f}" for you in you_acc]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def plot_err(it_sev, you_sev):
    labels = ["baseline"] + [str(i) for i in range(200, (len(it_sev) + 1) * 100, 100)]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 5))
    rects1 = ax.bar(x - width / 2, it_sev, width, label='It')
    rects2 = ax.bar(x + width / 2, you_sev, width, label='You')

    ax.set_ylabel('Error severity')
    title = sys.argv[1].replace("/", " (").replace("unbalanced", "original") + ")" if sys.argv[1][:3] == "TED" else sys.argv[1]
    ax.set_title(f'Error severity for {title}')
    ax.set_ylim([1, 10])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    for rect, label in zip(rects1, [f"{it:.2f}" for it in it_sev]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    for rect, label in zip(rects2, [f"{you:.2f}" for you in you_sev]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def plot_cer(it_cer, you_cer):
    labels = ["baseline"] + [str(i) for i in range(200, (len(it_cer) + 1) * 100, 100)]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 5))
    rects1 = ax.bar(x - width / 2, it_cer, width, label='It')
    rects2 = ax.bar(x + width / 2, you_cer, width, label='You')

    ax.set_ylabel('Certainty')
    title = sys.argv[1].replace("/", " (").replace("unbalanced", "original") + ")" if sys.argv[1][:3] == "TED" else sys.argv[1]
    ax.set_title(f'Certainty for {title}')
    ax.set_ylim([2, 10])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    for rect, label in zip(rects1, [f"{it:.2f}" for it in it_cer]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    for rect, label in zip(rects2, [f"{you:.2f}" for you in you_cer]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def plot_prf1(prec, rec, f1, label="it"):
    labels = ["baseline"] + [str(i) for i in range(200, (len(it_cer) + 1) * 100, 100)]

    x1 = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    x2 = [x + width for x in x1]
    x3 = [x + width for x in x2]

    fig, ax = plt.subplots(figsize=(14, 5))
    rects1 = ax.bar(x1, prec, width, label='Precision')
    rects2 = ax.bar(x2, rec, width, label='Recall')
    rects3 = ax.bar(x3, f1, width, label='F1-score')

    ax.set_ylabel('Score')
    title = sys.argv[1].replace("/", " (").replace("unbalanced", "original") + ")" if sys.argv[1][:3] == "TED" else sys.argv[1]
    ax.set_title(f'"{label}" macro average precision, recall and F1-score for {title}')
    ax.set_ylim([0, 1])
    ax.set_xticks(x2)
    ax.set_xticklabels(labels)
    ax.legend()

    for rect, label in zip(rects1, [f"{p:.2f}" for p in prec]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom', fontsize='small')

    for rect, label in zip(rects2, [f"{r:.2f}" for r in rec]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom', fontsize='small')

    for rect, label in zip(rects3, [f"{f:.2f}" for f in f1]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom', fontsize='small')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        get_results(sys.argv[1], sys.argv[2])
    else:
        context_range = 900 if sys.argv[1] == "OpenSubtitles" else 1100
        res_dict = {}
        for c in [0] + list(range(200, context_range, 100)):
            res_dict[c] = get_results(sys.argv[1], str(c))

        it_acc, you_acc = [res_dict[key]["it"]["acc"] for key in res_dict], [res_dict[key]["you"]["acc"] for key in res_dict]
        it_sev, you_sev = [res_dict[key]["it"]["sev"] for key in res_dict], [res_dict[key]["you"]["sev"] for key in res_dict]
        it_cer, you_cer = [res_dict[key]["it"]["cert"] for key in res_dict], [res_dict[key]["you"]["cert"] for key in res_dict]

        it_prec, it_rec, it_f1 = [res_dict[key]["it"]["cr"]["macro avg"]["precision"] for key in res_dict],\
                                 [res_dict[key]["it"]["cr"]["macro avg"]["recall"] for key in res_dict],\
                                 [res_dict[key]["it"]["cr"]["macro avg"]["f1-score"] for key in res_dict]

        you_prec, you_rec, you_f1 = [res_dict[key]["you"]["cr"]["macro avg"]["precision"] for key in res_dict], \
                                 [res_dict[key]["you"]["cr"]["macro avg"]["recall"] for key in res_dict], \
                                 [res_dict[key]["you"]["cr"]["macro avg"]["f1-score"] for key in res_dict]


        # plot_acc(it_acc, you_acc)
        plot_err(it_sev, you_sev)
        # plot_cer(it_cer, you_cer)
        # plot_prf1(it_prec, it_rec, it_f1)
        # plot_prf1(you_prec, you_rec, you_f1, label="you")

