from .eos_cli_config_gen import eos_cli_config_gen
from .eos_designs_facts import eos_designs_facts
from .eos_designs_structured_configs import eos_designs_structured_configs
import importlib.metadata


""" Library for running Arista Validated Designs (AVD) in Python
"""
DESCRIPTION = __doc__
NAME = "pyavd"

__author__ = "Arista Networks"
__copyright__ = "Copyright 2023 Arista Networks"
__license__ = "Apache 2.0"
__version__ = importlib.metadata.version(NAME)

__all__ = ["eos_cli_config_gen", "eos_designs_facts", "eos_designs_structured_configs"]
