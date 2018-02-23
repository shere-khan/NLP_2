import unittest
from data import match


class TestStringAlignment(unittest.TestCase):

    def setUp(self):
        self.r = match.Rules()

    def test_ses(self):
        s = "aaases"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaase")

    def test_zes(self):
        s = "aaazes"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaaze")

    def test_sess(self):
        s = "aaasses"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaass")

    def test_xes(self):
        s = "aaaxes"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaax")

    def test_ches(self):
        s = "aaaches"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaach")

    def test_shes(self):
        s = "aaashes"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaash")

    def test_men(self):
        s = "aamen"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "aaman")

    def test_ies(self):
        s = "cherries"
        s = self.r.lemmatize(s)

        self.assertEqual(s, "cherry")
