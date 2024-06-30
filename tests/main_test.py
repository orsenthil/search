import argparse
import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from fastapi import Request

from main import app, get_top_urls, main, parse_args, read_about, search, search_results


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

    @patch("main.engine")
    @patch("main.templates")
    async def test_search_results(self, mock_templates, mock_engine):
        # Setup mock for engine.search
        mock_engine.search.return_value = {
            "url1": 10,
            "url2": 9,
            "url3": 8,
            "url4": 7,
            "url5": 6,
            "url6": 5,
            "url7": 4,
            "url8": 3,
            "url9": 2,
            "url10": 1,
        }

        mock_response = MagicMock()
        mock_templates.TemplateResponse.return_value = mock_response

        mock_request = MagicMock(spec=Request)

        response = await search_results(mock_request, "test_query")

        mock_templates.TemplateResponse.assert_called_once_with(
            "results.html",
            {
                "request": mock_request,
                "results": {"url1": 10, "url2": 9, "url3": 8, "url4": 7, "url5": 6},
                "query": "test_query",
            },
        )

        self.assertEqual(response, mock_response)

    @patch("main.templates")
    def test_about(self, mock_templates):
        mock_response = MagicMock()
        mock_templates.TemplateResponse.return_value = mock_response

        mock_request = MagicMock(spec=Request)

        response = read_about(mock_request)

        mock_templates.TemplateResponse.assert_called_once_with("about.html", {"request": mock_request})

        self.assertEqual(response, mock_response)

    @patch("main.parse_args")
    @patch("main.pd.read_parquet")
    @patch("main.engine.bulk_index")
    @patch("main.run")
    def test_main_snippet(self, mock_run, mock_bulk_index, mock_read_parquet, mock_parse_args):
        mock_parse_args.return_value = MagicMock(data_path="test/path")

        mock_data_frame = MagicMock()
        mock_data_frame.__getitem__.side_effect = lambda x: MagicMock(
            values=["Example Content"] if x == "content" else ["http://example.com"]
        )

        mock_read_parquet.return_value = mock_data_frame

        # Execute the code under test
        main()

        # Assert that read_parquet was called with the correct path
        mock_read_parquet.assert_called_once_with("test/path")

        # Assert that bulk_index was called with the correct content
        content = list(zip(["http://example.com"], ["Example Content"]))
        mock_bulk_index.assert_called_once_with(content)

        # Assert that run was called with the correct arguments
        mock_run.assert_called_once_with(app, host="127.0.0.1", port=80)
