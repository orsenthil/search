from main import get_top_urls


def test_get_top_urls():
    scores_dict = {"url1": 10, "url2": 5, "url3": 8, "url4": 3, "url5": 6}
    n = 3

    expected_result = {"url1": 10, "url3": 8, "url5": 6}
    assert get_top_urls(scores_dict, n) == expected_result
