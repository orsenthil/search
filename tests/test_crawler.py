import unittest
from unittest.mock import MagicMock, patch

from crawler import parse_feed


class TestParseFeed(unittest.TestCase):
    @patch("crawler.feedparser.parse")
    def test_parse_feed_success(self, mock_parse):
        # Setup mock
        mock_parse.return_value = MagicMock(entries=[MagicMock(link="http://example.com")])

        # Call the function
        result = parse_feed("http://feed_url.com")

        # Assert the expected outcome
        self.assertEqual(result, ["http://example.com"])

    @patch("crawler.feedparser.parse")
    def test_parse_feed_exception(self, mock_parse):
        # Setup mock to raise an exception
        mock_parse.side_effect = Exception("Some error")

        # Call the function
        result = parse_feed("http://feed_url.com")

        # Assert the function handles exceptions as expected
        self.assertRaises(Exception, result)
