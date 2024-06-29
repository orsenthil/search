import argparse
import unittest
from unittest.mock import patch

from main import get_top_urls, parse_args


def test_get_top_urls():
    scores_dict = {"url1": 10, "url2": 5, "url3": 8, "url4": 3, "url5": 6}
    n = 3

    expected_result = {"url1": 10, "url3": 8, "url5": 6}
    assert get_top_urls(scores_dict, n) == expected_result


class TestParseArgs(unittest.TestCase):
    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_args(self, mock_parse_args):
        # Mock the return value of parse_args to simulate command line argument parsing
        mock_parse_args.return_value = argparse.Namespace(data_path="test/path")

        # Call the function under test
        args = parse_args()
        # Assert that the data_path argument is correctly parsed
        self.assertEqual(args.data_path, "test/path")
