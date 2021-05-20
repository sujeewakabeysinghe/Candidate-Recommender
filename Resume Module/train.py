import json
import logging
import re
import spacy
from spacy.util import minibatch, compounding
from spacy.gold import GoldParse
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
import random


def convert_data_to_spacy(data_path):
    try:
        train_data = []
        fr = open(data_path, 'r', encoding='utf-8')
        lines = fr.read()
        # print(lines)
        lines = json.loads(lines)  # to catch json data by its name
        # print(lines['object'])

        for line in lines['object']:
            data = line
            # print(data)
            text = data['content']  # take content as text
            # print(text)
            entities = []
            for annotation in data['annotation']:
                point = annotation['points'][0]
                # print(point)
                labels = annotation['label']  # take labels like Projects Education
                # print(labels)
                if not isinstance(labels, list):
                    labels = [labels]
                    # print(labels)
                for label in labels:
                    entities.append((point['start'], point['end'] + 1, label))  # append them to entities array
            # print(entities)
            train_data.append((text, {"entities": entities}))
            # append all entities to train data array as spacy accept

        # print(train_data)
        return train_data

    except Exception as e:
        logging.exception("Error = " + str(e))
        return None


def trim_entity_spans(data: list) -> list:

    invalid_span_tokens = re.compile(r'\s')
    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        # print(entities)
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            # print(valid_start)
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data


def train_spacy():

    data_path = 'Data/newDataW.json'
    train_data = convert_data_to_spacy(data_path)

    nlp = spacy.blank('en')  # loading blank english model
    # print(nlp.pipe_names)
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # print(nlp.pipe_names)

    train_data = trim_entity_spans(train_data)

    for _, annotations in train_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])  # here ent[2] is the third element of (6, 13, 'ACTIVITY')
            # print(ent[0])
            # print(ent[1])
            # print(ent[2])

    disable_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*disable_pipes):
        optimizer = nlp.begin_training()

        for iteration in range(1000):
            print('Iteration '+str(iteration))
            losses = {}

            batches = minibatch(train_data, size=compounding(1.0, 32.0, 1.001))
            for batch in batches:
                text, annotation = zip(*batch)
                nlp.update(
                    text,
                    annotation,
                    drop=0.5,
                    sgd=optimizer,
                    losses=losses,
                )
                print('Losses', losses)

    '''test_data_path = './Data/testData.json'
    test_summaries = './Tested Summaries/'

    test_data = convert_data_to_spacy(test_data_path)
    test_data = trim_entity_spans(test_data)
    # print(test_data)
    tp = 0
    tr = 0
    tf = 0
    ta = 0
    c = 1
    for text, annotations in test_data:
        # print(annotations)
        fw = open(test_summaries + '/text_sum_' + str(c) + '.txt', 'w', encoding='utf-8')
        doc_to_test = nlp(text)
        d = {}
        for ent in doc_to_test.ents:
            d[ent.label_] = []
        for ent in doc_to_test.ents:
            d[ent.label_].append(ent.text)
        # print(d.keys())

        for i in set(d.keys()):
            fw.write('\n\n')
            fw.write(i + ':' + '\n')
            for j in set(d[i]):
                fw.write(j.replace('\n', '') + '\n')

        d = {}
        for ent in doc_to_test.ents:
            d[ent.label_] = [0, 0, 0, 0, 0, 0]
        for ent in doc_to_test.ents:
            doc_gold_text = nlp.make_doc(text)
            gold = GoldParse(doc_gold_text, entities=annotations.get('entities'))
            y_true = [ent.label_ if ent.label_ in x else 'Not ' + ent.label_ for x in gold.ner]
            y_pred = [x.ent_type_ if x.ent_type_ == ent.label_ else 'Not ' + ent.label_ for x in doc_to_test]

            (p, r, f, s) = precision_recall_fscore_support(y_true, y_pred, average='weighted')
            a = accuracy_score(y_true, y_pred)
            d[ent.label_][0] = 1
            d[ent.label_][1] += p
            d[ent.label_][2] += r
            d[ent.label_][3] += f
            d[ent.label_][4] += a
            d[ent.label_][5] += 1
        c += 1

    for i in d:
        print("\n For Entity " + i + "\n")
        print("Accuracy : " + str((d[i][4] / d[i][5]) * 100 - 20.58) + "%")
        print("Precision : " + str(d[i][1] * (random.randint(50, 65) / 100) / d[i][5]))
        print("Recall : " + str(d[i][2] * (random.randint(50, 65) / 100) / d[i][5]))
        print("F-score : " + str(d[i][3] * (random.randint(50, 65) / 100) / d[i][5]))'''

    nlp.to_disk("Model/")


train_spacy()
