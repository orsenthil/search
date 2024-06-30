import argparse
import asyncio
import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp

from crawler import clean_content, fetch_content, parse_args, parse_feed, process_feed


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


class TestParseArgs(unittest.TestCase):
    @patch("crawler.argparse.ArgumentParser.parse_args")
    def test_parse_args_feed_path(self, mock_parse_args):
        # Mock the return value of parse_args to simulate command line input
        mock_parse_args.return_value = argparse.Namespace(feed_path="test_feed.xml")

        # Call the function under test
        args = parse_args()

        # Assert that the feed-path argument is correctly parsed
        self.assertEqual(args.feed_path, "test_feed.xml")


class TestFetchContent(IsolatedAsyncioTestCase):
    @patch("crawler.aiohttp.ClientSession.get")
    async def test_fetch_content(self, mock_get):
        # Mock the response of session.get to return an object with an async text() method
        mock_response = AsyncMock()
        mocked_response_text = "Mocked content"
        mock_response.text = AsyncMock(return_value=mocked_response_text)
        mock_get.return_value.__aenter__.return_value = mock_response

        # Create a mock session and URL for testing
        async with aiohttp.ClientSession() as session:
            url = "http://example.com"

            # Call the function under test
            content = await fetch_content(session, url)

            # Assert that the content returned is as expected
            mock_get.assert_called_once_with(url)
            self.assertEqual(content, mocked_response_text)

    async def asyncSetUp(self):
        self.loop = asyncio.get_event_loop()

    @patch("crawler.parse_feed")
    @patch("crawler.fetch_content")
    @patch("crawler.clean_content")
    async def test_process_feed(self, mock_clean_content, mock_fetch_content, mock_parse_feed):
        # Setup mock return values
        mock_parse_feed.return_value = ["http://example.com/post1", "http://example.com/post2"]
        mock_fetch_content.side_effect = lambda session, url: f"Content for {url}"
        mock_clean_content.side_effect = lambda content: f"Cleaned {content}"

        # Expected result after processing
        expected = [
            ("http://example.com/post1", "Cleaned Content for http://example.com/post1"),
            ("http://example.com/post2", "Cleaned Content for http://example.com/post2"),
        ]

        # Run the process_feed function
        session = MagicMock()  # Mock session object
        result = await process_feed("http://example.com/feed", session, self.loop)

        # Assert the result matches expected output
        self.assertEqual(result, expected)
