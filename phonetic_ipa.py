from collections import Counter
from math import sqrt
import eng_to_ipa as ipa
# import itertools
# import pandas as pd


# df = pd.read_csv("Locality_village_pincode_final_mar-2017.csv", encoding="ISO-8859-1")
# pincode_count = df.Pincode.value_counts()
# pincode = 0
# for pin_code in pincode_count.iteritems():
#     pincode = pin_code[0]
#     break
#
# area_list = df[df.Pincode == pincode]["Village/Locality name"].unique()
# try:
#     pass
# except Exception as e:
#     print('Got exception', e)


def word2vec(word):
    cw = Counter(word)
    sw = set(cw)
    lw = sqrt(sum(c * c for c in cw.values()))
    return cw, sw, lw


def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]


# list_A = ['Abdulpur', 'Seetalpur colliery', 'Radhanagar', 'Chinakuri', 'Ahmedabad']
# list_B = ['abadulpore']


def check_similarity(input_word, area_list):
    IPA_input_word = ipa.convert(input_word)
    IPA_area_list = [ipa.convert(each) for each in area_list]
    score_list = []
    for area in IPA_area_list:
        res = cosdis(word2vec(input_word), word2vec(area))
        score_list.append(res)
    return score_list


def compare_similarity(input_word, area_list):
    return check_similarity(input_word, area_list)
