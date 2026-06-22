"""
Tests for enum case alignment (P6).

DB stores uppercase values ('UPLOADED', 'AI', etc).
Python enum values must match exactly or SQLAlchemy will fail on read.
"""
import pytest
from app.models.budget_templates import UploadedTemplateStatus
from app.models.mapping import MappingSource


class TestUploadedTemplateStatus:
    def test_values_are_uppercase(self):
        for member in UploadedTemplateStatus:
            assert member.value == member.value.upper(), (
                f"{member.name} has value '{member.value}', expected uppercase"
            )

    def test_uploaded_value(self):
        assert UploadedTemplateStatus.UPLOADED == "UPLOADED"

    def test_detected_value(self):
        assert UploadedTemplateStatus.DETECTED == "DETECTED"

    def test_mapped_value(self):
        assert UploadedTemplateStatus.MAPPED == "MAPPED"

    def test_consumed_value(self):
        assert UploadedTemplateStatus.CONSUMED == "CONSUMED"

    def test_roundtrip_from_db_string(self):
        # Simulate reading the DB value back into the enum
        assert UploadedTemplateStatus("UPLOADED") == UploadedTemplateStatus.UPLOADED

    def test_lowercase_db_string_raises(self):
        with pytest.raises(ValueError):
            UploadedTemplateStatus("uploaded")


class TestMappingSource:
    def test_values_are_uppercase(self):
        for member in MappingSource:
            assert member.value == member.value.upper(), (
                f"{member.name} has value '{member.value}', expected uppercase"
            )

    def test_ai_value(self):
        assert MappingSource.AI == "AI"

    def test_human_value(self):
        assert MappingSource.HUMAN == "HUMAN"

    def test_rule_value(self):
        assert MappingSource.RULE == "RULE"

    def test_imported_value(self):
        assert MappingSource.IMPORTED == "IMPORTED"

    def test_roundtrip_from_db_string(self):
        assert MappingSource("AI") == MappingSource.AI

    def test_lowercase_db_string_raises(self):
        with pytest.raises(ValueError):
            MappingSource("ai")
