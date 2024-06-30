import unittest

from search import normalize_string, update_url_scores


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

    def test_update_url_scores(self):
        old_scores = {
            "example.com": 10,
            "google.com": 5,
        }
        new_scores = {
            "example.com": 5,
            "github.com": 3,
        }
        expected_scores = {
            "example.com": 15,
            "google.com": 5,
            "github.com": 3,
        }
        self.assertEqual(update_url_scores(old_scores, new_scores), expected_scores)
