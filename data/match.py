import re


class Rules:
    def __init__(self):
        self.was_rule_applied = False

    def rule_sses(self, s):
        exp = r'(?<=[\w])sses$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_xes(self, s):
        exp = r'(?<=[\w])xes$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_ses(self, s):
        exp = r'(?<=[\w])ses$'
        match = re.search(exp, s)
        if match:
            s = s[:-1]
            self.was_rule_applied = True

        return s

    def rule_zes(self, s):
        exp = r'(?<=[\w])zes$'
        match = re.search(exp, s)
        if match:
            s = s[:-1]
            self.was_rule_applied = True

        return s

    def rule_ches(self, s):
        exp = r'(?<=[\w])ches$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_shes(self, s):
        exp = r'(?<=[\w])shes$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_men(self, s):
        exp = r'(?<=[\w])men$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            s += 'an'
            self.was_rule_applied = True

        return s

    def rule_ies(self, s):
        exp = r'(?<=[\w])ies$'
        match = re.search(exp, s)
        if match:
            s = s[:-3]
            s += 'y'
            self.was_rule_applied = True

        return s

    def lemmatize(self, s):
        s = self.rule_ches(s)
        if not self.was_rule_applied:
            s = self.rule_ies(s)
        if not self.was_rule_applied:
            s = self.rule_men(s)
        if not self.was_rule_applied:
            s = self.rule_sses(s)
        if not self.was_rule_applied:
            s = self.rule_ses(s)
        if not self.was_rule_applied:
            s = self.rule_shes(s)
        if not self.was_rule_applied:
            s = self.rule_xes(s)
        if not self.was_rule_applied:
            s = self.rule_zes(s)

        return s
