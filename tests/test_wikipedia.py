"""Tests for returning a random Wikipedia page."""

from unittest.mock import Mock

import click
import pytest

from hypermodern_pc import wikipedia


def test_random_page_uses_given_language(mock_requests_get: Mock) -> None:
    """Check that language is used when provided."""
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]


def test_random_page_returns_page(mock_requests_get: Mock) -> None:
    """Test random page returns a Wikipedia page."""
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    """Test random page exceptions."""
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


# Temporary to trigger Typeguard error
# def test_trigger_typeguard(mock_requests_get):
#     import json
#     data = json.loads('{ "language": 1 }')
#     wikipedia.random_page(language=data["language"])
