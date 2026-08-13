import pytest

from core.ads.continent_slug import UNMAPPED_SLUG, continent_slug


class TestContinentSlug:
    def test_returns_unmapped_when_none(self):
        assert continent_slug(None) == UNMAPPED_SLUG

    def test_returns_unmapped_when_empty_string(self):
        assert continent_slug("") == UNMAPPED_SLUG

    def test_lowercases_continent_code(self):
        assert continent_slug("NA") == "na"

    def test_already_lowercase_code_is_unchanged(self):
        assert continent_slug("eu") == "eu"

    def test_mixed_case_code_is_lowercased(self):
        assert continent_slug("As") == "as"

    @pytest.mark.parametrize(
        "code,expected",
        [
            ("NAM", "nam"),
            ("SAM", "sam"),
            ("EUR", "eur"),
            ("AS", "as"),
            ("AFR", "afr"),
            ("OC", "oc"),
            ("AN", "an"),
        ],
    )
    def test_all_continent_codes(self, code, expected):
        assert continent_slug(code) == expected
