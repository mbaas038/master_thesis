import os
import xml.etree.ElementTree as ET


if __name__ == '__main__':
    DEV_DIR = "/data/s3212262/thesis_data/TED5/dev"
    tree_en = ET.parse(os.path.join(DEV_DIR, 'IWSLT17.TED.dev2010.en-nl.en.xml'))
    root_en = tree_en.getroot()
    for doc in root_en.find("srcset"):
        doc_id = doc.find("talkid").text
        os.mkdir(os.path.join(DEV_DIR, doc_id))
        en_out = open(os.path.join(DEV_DIR, doc_id, "en.raw"), "w", encoding="utf-8")
        for sent in doc.findall("seg"):
            en_out.write(sent.text.strip()+"\n")
        en_out.close()
    tree_nl = ET.parse(os.path.join(DEV_DIR, 'IWSLT17.TED.dev2010.en-nl.nl.xml'))
    root_nl = tree_nl.getroot()
    for doc in root_nl.find("refset"):
        doc_id = doc.find("talkid").text
        nl_out = open(os.path.join(DEV_DIR, doc_id, "nl.raw"), "w", encoding="utf-8")
        for sent in doc.findall("seg"):
            nl_out.write(sent.text.strip() + "\n")
        nl_out.close()

