import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch
from web.utils import find_top_matches, extract_pdf_text

def test_find_top_matches_returns_correct_number_and_uniqueness():
    test_cv_text = "la mia esperienza include python, java, e project management. sono un software engineer."
    k_results = 5

    top_matches = find_top_matches(cv_text=test_cv_text, k=k_results)

    assert len(top_matches) == k_results, f"Expected {k_results} results, but got {len(top_matches)}"
    
    job_links = [job['Job Link'] for job in top_matches]
    assert len(job_links) == len(set(job_links)), "Found duplicate job links in results"


@patch('web.utils.extract_text')
def test_extract_pdf_text_with_mock(mock_extract_text):
    pdf_path = "dummy/path/to/cv.pdf"
    raw_text = "Test CV content with python and java SKILLS"
    mock_extract_text.return_value = raw_text

    processed_text = extract_pdf_text(pdf_path)

    mock_extract_text.assert_called_once_with(pdf_path)

    expected_text = "test cv content python java"
    assert processed_text == expected_text