import os
from config.config import Configuration


def test_load_configuration():
    """Test loading configuration from file"""

    Configuration.force_config_file(
        os.path.join(os.path.dirname(__file__), "test.config")
    )

    assert Configuration.get("identification", "company") == "TestCompany"
    assert Configuration.get("billing", "invoices_path") == "TEST"


# TODO test more configuration aspects, for example invoice pattern parsing
