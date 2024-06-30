import unittest
from unittest.mock import MagicMock, patch

from crawler import clean_content, parse_feed


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


class TestCleanContent(unittest.TestCase):
    def test_clean_content(self):
        # Mock HTML content with script, style tags, and some text
        html_content = """
        <html>
            <head>
                <title>Test HTML</title>
                <style>body {background-color: powderblue;}</style>
            </head>
            <body>
                <script>alert("Hello, world!");</script>
                <p>This is a <b>test</b> paragraph.</p>
                <p>This is another test paragraph with <a href="#">a link</a>.</p>
            </body>
        </html>
        """
        # Expected output after cleaning the HTML content
        expected_output = "Test HTML This is a test paragraph. This is another test paragraph with a link."

        # Call the clean_content function with the mock HTML content
        result = clean_content(html_content)

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()