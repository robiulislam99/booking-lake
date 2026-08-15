import pytest

from core.ads.csv_writer import CSV_HEADER, render_ad_campaign_csv


class TestRenderAdCampaignCsv:
    def test_header_only_when_no_records(self):
        result = render_ad_campaign_csv([])
        assert result == "Page URL,Custom label\n"

    def test_single_record(self):
        records = [{"Page URL": "https://example.com/hotel-1", "Custom label": "beach"}]
        result = render_ad_campaign_csv(records)
        assert result == "Page URL,Custom label\nhttps://example.com/hotel-1,beach\n"

    def test_multiple_records_preserve_order(self):
        records = [
            {"Page URL": "https://example.com/a", "Custom label": "city"},
            {"Page URL": "https://example.com/b", "Custom label": "resort"},
        ]
        result = render_ad_campaign_csv(records)
        lines = result.splitlines()
        assert lines[0] == "Page URL,Custom label"
        assert lines[1] == "https://example.com/a,city"
        assert lines[2] == "https://example.com/b,resort"

    def test_uses_lf_line_terminator(self):
        records = [{"Page URL": "https://example.com/a", "Custom label": "city"}]
        result = render_ad_campaign_csv(records)
        assert "\r\n" not in result
        assert result.endswith("\n")

    def test_field_containing_comma_is_quoted(self):
        records = [{"Page URL": "https://example.com/a", "Custom label": "city, beach"}]
        result = render_ad_campaign_csv(records)
        assert '"city, beach"' in result

    def test_field_containing_quote_is_escaped(self):
        records = [{"Page URL": "https://example.com/a", "Custom label": 'the "best"'}]
        result = render_ad_campaign_csv(records)
        assert '"the ""best"""' in result

    def test_field_containing_newline_is_quoted(self):
        records = [{"Page URL": "https://example.com/a", "Custom label": "line1\nline2"}]
        result = render_ad_campaign_csv(records)
        assert '"line1\nline2"' in result

    def test_missing_page_url_key_raises_keyerror(self):
        records = [{"Custom label": "city"}]
        with pytest.raises(KeyError):
            render_ad_campaign_csv(records)

    def test_missing_custom_label_key_raises_keyerror(self):
        records = [{"Page URL": "https://example.com/a"}]
        with pytest.raises(KeyError):
            render_ad_campaign_csv(records)

    def test_header_constant_matches_output_header(self):
        result = render_ad_campaign_csv([])
        assert result.splitlines()[0] == ",".join(CSV_HEADER)
