import unittest

from search import SearchEngine, normalize_string, update_url_scores


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


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.search_engine = SearchEngine(k1=1.5, b=0.75)
        self.search_engine.bulk_index(
            [
                ("example.com", "Hello world"),
                ("google.com", "Hello, world!"),
                ("github.com", "Hello  world"),
            ]
        )

    def test_number_of_documents(self):
        self.assertEqual(self.search_engine.number_of_documents, 3)

    def test_posts(self):
        self.assertEqual(self.search_engine.posts, ["example.com", "google.com", "github.com"])

    def test_avdl(self):
        self.assertAlmostEqual(self.search_engine.avdl, 12.00, places=2)

    def test_idf(self):
        self.assertAlmostEqual(self.search_engine.idf("hello"), 0.13, places=2)
        self.assertAlmostEqual(self.search_engine.idf("world"), 0.133, places=2)
        self.assertAlmostEqual(self.search_engine.idf("example"), 2.079, places=2)
        self.assertAlmostEqual(self.search_engine.idf("google"), 2.079, places=2)
        self.assertAlmostEqual(self.search_engine.idf("github"), 2.079, places=2)

    def test_bm25(self):
        keys = ["example.com", "google.com", "github.com"]
        expected_scores = {
            "example.com": 0.13873391441508837,
            "google.com": 0.13353139262452257,
            "github.com": 0.12870495674652777,
        }
        for key in keys:
            self.assertAlmostEqual(self.search_engine.bm25("hello")[key], expected_scores[key], places=2)

        expected_scores = {
            "example.com": 0.13873391441508837,
            "google.com": 0.13353139262452257,
            "github.com": 0.12870495674652777,
        }
        for key in keys:
            self.assertAlmostEqual(self.search_engine.bm25("world")[key], expected_scores[key], places=2)

    def test_search(self):
        keys = ["example.com", "google.com", "github.com"]
        expected_scores = {
            "example.com": 0.13873391441508837,
            "google.com": 0.13353139262452257,
            "github.com": 0.12870495674652777,
        }

        for key in keys:
            self.assertAlmostEqual(self.search_engine.search("hello")[key], expected_scores[key], places=2)

        for key in keys:
            self.assertAlmostEqual(self.search_engine.search("world")[key], expected_scores[key], places=2)
