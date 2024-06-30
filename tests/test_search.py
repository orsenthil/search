import unittest

from search import normalize_string


class TestNormalizeString(unittest.TestCase):
    def test_normalize_string_no_punctuation(self):
        input_expected_pairs = [
            ("Hello world", "hello world"),
            ("Hello, world!", "hello world"),
            ("Hello  world", "hello world"),
            ("", ""),
        ]
        for input_string, expected_output in input_expected_pairs:
            with self.subTest(input_string=input_string):
                self.assertEqual(normalize_string(input_string), expected_output)
