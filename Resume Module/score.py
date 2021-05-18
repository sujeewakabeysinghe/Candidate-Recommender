import json
import string
import re
import spacy
import random
import io
import csv

text_path = './Doc/'
data = [
    ['Skills' 'C++', 'Java', 'Angular'],
    ['Skills' 'C++', 'Java', 'Angular'],
    ['Education' 'C++', 'Java', 'Angular']
]


def text_to_list(name):
    fr = open(text_path + name, 'r', encoding='utf-8')  # reading score text file
    # text = fr.read()
    # print(text)
    skill_list = []
    for line in fr.readlines():
        skill_list.append(line.rstrip())
    # print(skill_list)
    return skill_list


# SE skill lists
'''SE_SKILL_LV1 = text_to_list("skill-se-level1")
SE_SKILL_LV2 = text_to_list("skill-se-level2")
SE_SKILL_LV3 = text_to_list("skill-se-level3")

# QA skill list
QA_SKILL_LV1 = text_to_list("skill-qa-level1")
QA_SKILL_LV2 = text_to_list("skill-qa-level2")
QA_SKILL_LV3 = text_to_list("skill-qa-level3")

# Experience
SE_EXPERIENCE = text_to_list("se-experience")
QA_EXPERIENCE = text_to_list("qa-experience")

# Designation
SE_DESIGNATION = text_to_list("se-designation")
QA_DESIGNATION = text_to_list("qa-designation")

# Education
EDUCATION = text_to_list("education")'''


def list_to_string(lists):
    str1 = ""
    content = str1.join(lists)
    # print(content)
    return content


def sentence_to_vec(content):
    candidate_pos = ['NOUN', 'PROPN']
    sentence = []
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(content)
    for sent in doc.sents:
        selected_words = []
        for token in sent:
            if token.pos_ in candidate_pos and token.is_stop is False:
                selected_words.append(token)
        sentence.append(selected_words)
    return sentence


def sentence_to_chunk(content):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(content)
    selected_nouns = []
    for noun in doc.noun_chunks:
        selected_nouns.append(noun)
    return selected_nouns


def count_score(l1, l2):
    c = 0
    for i in l1:
        for j in l2:
            if i == j:
                c += 1
    return c


def score_skills():
    if data[0] is not None:
        print(data)
        return 50
    else:
        return None


score_skills()
