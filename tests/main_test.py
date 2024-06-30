import argparse
import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from fastapi import Request

from main import get_top_urls, parse_args, search


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


class TestSearchFunction(IsolatedAsyncioTestCase):
    @patch("main.engine")
    @patch("main.templates")
    async def test_search(self, mock_templates, mock_engine):
        # Setup mock for engine.posts
        mock_engine.posts = ["post1", "post2"]

        # Setup mock for templates.TemplateResponse
        mock_response = MagicMock()
        mock_templates.TemplateResponse.return_value = mock_response

        # Create a mock request object
        mock_request = MagicMock(spec=Request)

        # Call the search function
        response = await search(mock_request)

        # Assert TemplateResponse was called with the correct template and context
        mock_templates.TemplateResponse.assert_called_once_with(
            "search.html", {"request": mock_request, "posts": ["post1", "post2"]}
        )

        # Assert the response is correct
        self.assertEqual(response, mock_response)
