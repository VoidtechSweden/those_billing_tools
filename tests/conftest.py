import configparser
import contextlib
import os
import tempfile

from config.config import Configuration

CONFIG_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../template.config")


@contextlib.contextmanager
def temporary_config(updated_fields=[], invalid=False):
    """Create and use temporary configuration file for testing purposes."""

    config = configparser.ConfigParser()
    config.read(CONFIG_TEMPLATE_PATH)

    for section, option, value in updated_fields:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)

    if invalid:
        config.remove_option("identification", "company")

    with tempfile.NamedTemporaryFile(
        prefix="temp_config_",
        mode="w+",
        delete=True,
        delete_on_close=False,
        suffix=".config",
    ) as tmp:
        config.write(tmp)
        tmp.flush()
        tmp.seek(0)
        Configuration.instance(tmp.name).reload_config_file(
            tmp.name
        )  # Needed to reload singleton
        yield
