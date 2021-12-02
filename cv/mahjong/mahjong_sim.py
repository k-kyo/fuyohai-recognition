import json
import os
from math import sqrt
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent


def hai_distance(distance_data, a, b):
    if a == b:
        return 0.
    elif 'z' == a[1]:
        return distance_data['字牌'][f'{b[0]}-z']
    elif 'z' == b[1]:
        return distance_data['字牌'][f'{a[0]}-z']
    elif a[1] == b[1]:
        return distance_data['同種'][f'{a[0]}-{b[0]}']
    elif ('m' == a[1] and 'p' == b[1]) or ('p' == a[1] and 'm' == b[1]):
        return distance_data['異種'][f'{a}-{b}'] if 'm' == a[1] else distance_data['異種'][f'{b}-{a}']
    elif ('p' == a[1] and 's' == b[1]) or ('s' == a[1] and 'p' == b[1]):
        return distance_data['異種'][f'{a}-{b}'] if 'p' == a[1] else distance_data['異種'][f'{b}-{a}']
    elif ('s' == a[1] and 'm' == b[1]) or ('m' == a[1] and 's' == b[1]):
        return distance_data['異種'][f'{a}-{b}'] if 's' == a[1] else distance_data['異種'][f'{b}-{a}']
    else:
        raise ValueError("error!")


def sutehai_distance(distance_data, a, b):
    return sum([hai_distance(distance_data, i.lower(), j.lower()) for i, j in zip(a, b)])


def sutehai_sim(query):
    with open(str(CURRENT_DIR / 'data/result.json'), mode='r', encoding='utf-8') as f:
        data = json.load(f)
    with open(str(CURRENT_DIR / 'data/distance.json'), mode='r', encoding='utf-8') as f:
        distance_data = json.load(f)


    dic = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    suit_dic = {'1m': 0, '2m': 0, '3m': 0, '4m': 0, '5m': 0, '6m': 0, '7m': 0, '8m': 0, '9m': 0,
                '1p': 0, '2p': 0, '3p': 0, '4p': 0, '5p': 0, '6p': 0, '7p': 0, '8p': 0, '9p': 0,
                '1s': 0, '2s': 0, '3s': 0, '4s': 0, '5s': 0, '6s': 0, '7s': 0, '8s': 0, '9s': 0,
                '1z': 0, '2z': 0, '3z': 0, '4z': 0, '5z': 0, '6z': 0, '7z': 0,}

    for d in data:
        distance = sutehai_distance(distance_data, query, d['trash'])
        if distance < 28:
            dic[str(d['label'][0])] += 1
            if d['label'][0] != 0:
                continue
            for i in d['label'][1]:
                suit_dic[i] += 1
    dic['3'] = dic['3'] + dic['4'] + dic['5'] + dic['6'] + dic['7'] + dic['8']
    s = sum(suit_dic.values())
    for k, v in suit_dic.items():
        suit_dic[k] = v / s * 100
    return dic, suit_dic
