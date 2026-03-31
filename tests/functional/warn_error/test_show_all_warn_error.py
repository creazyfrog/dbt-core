import pytest

from dbt.tests.util import run_dbt
from dbt_common.exceptions import EventCompilationError


class TestShowAllWarnErrorsFalse:
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
            "flags": {
                "show_all_warn_errors": False,
            },
            "models": {
                "path1": {
                    "+enabled": True,
                },
                "path2": {
                    "+enabled": True,
                },
            },
        }

    def test_immediate_warn_error_only_first_in_message(self, project):
        with pytest.raises(EventCompilationError) as exc_info:
            run_dbt(["--warn-error", "parse"])
        msg = exc_info.value.msg
        assert "path1" in msg
        assert "path2" not in msg


class TestShowAllWarnErrorsTrue:
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
            "flags": {
                "show_all_warn_errors": True,
            },
            "models": {
                "path1": {
                    "+enabled": True,
                },
                "path2": {
                    "+enabled": True,
                },
            },
        }

    def test_deferred_warn_errors_combine_both_in_message(self, project):
        with pytest.raises(EventCompilationError) as exc_info:
            run_dbt(["--warn-error", "parse"])
        msg = exc_info.value.msg
        assert "path1" in msg
        assert "path2" in msg


class TestShowAllWarnErrorsOmittedDefaultsToFalse:
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
            "flags": {},
            "models": {
                "path1": {
                    "+enabled": True,
                },
                "path2": {
                    "+enabled": True,
                },
            },
        }

    def test_omitted_flag_matches_false(self, project):
        with pytest.raises(EventCompilationError) as exc_info:
            run_dbt(["--warn-error", "parse"])
        msg = exc_info.value.msg
        assert "path1" in msg
        assert "path2" not in msg
