import spacy
import json
from pdfToText import pdf_to_text_convert


image_dir = './Images/'
pdf_file = './CV/Ishara_De_Silva_SE.pdf'
model_path = './Model/'
text_file = './Texts'


def generate_info_file():
    pdf_to_text_convert(pdf_file, image_dir)  # convert pdf to text
    nlp = spacy.load('Model/')  # loading custom spacy model

    fr = open(text_file+'/text.txt', 'r', encoding='utf-8')  # reading generated text file
    text = fr.read()
    # print(text)

    fw = open(text_file+'/text_sum.txt', 'w', encoding='utf-8')  # writing it -
    doc = nlp(text)
    d = {}  # declare a data dic
    for ent in doc.ents:
        d[ent.label_] = []
    for ent in doc.ents:
        d[ent.label_].append(ent.text)
    # print(d)
    print(d.keys())  # keys are EDUCATION PROJECTS etc

    for i in set(d.keys()):
        fw.write('\n\n')
        fw.write(i+':'+'\n')
        for j in set(d[i]):
            fw.write(j.replace('\n', '')+'\n')
    fr.close()
    fw.close()

    data = {}
    for i in set(d.keys()):
        data[i] = []
    # print(data)

    for i in set(d.keys()):
        for j in set(d[i]):
            data[i].append(j)
    # print(data)

    entity_list = ['Name', 'Designation', 'Skills', 'Projects', 'Educations', 'Experience']
    extracted_list = list(data.keys())
    # print(entity_list)
    # print(extracted_list)
    diff = list(set(entity_list) - set(extracted_list))
    # print(diff)

    if diff != []:  # if something went wrong add !=
        for i in diff:
            data[i] = None
            # print(data[i])

    with open(text_file + "/out.json", 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return "success"


generate_info_file()
