import re


def rule_sess(s):
    exp = r'sess$'
    match = re.search(exp, s)
    if match:
        s = s[:-2]

    return s


def rule_xes(s):
    exp = r'xes$'
    match = re.search(exp, s)
    if match:
        s = s[:-2]

    return s


def rule_ses(s):
    exp = r'ses$'
    match = re.search(exp, s)
    if match:
        s = s[:-1]

    return s


def rule_zes(s):
    exp = r'zes$'
    match = re.search(exp, s)
    if match:
        s = s[:-1]

    return s


def rule_ches(s):
    exp = r'zes$'
    match = re.search(exp, s)
    if match:
        s = s[:-2]

    return s


def rule_shes(s):
    exp = r'shes$'
    match = re.search(exp, s)
    if match:
        s = s[:-2]

    return s


def rule_men(s):
    exp = r'men$'
    match = re.search(exp, s)
    if match:
        s = s[:-2]
    s += 'an'

    return s


def rule_ies(s):
    exp = r'ies$'
    match = re.search(exp, s)
    if match:
        s = s[:-3]
    s += 'y'

    return s
