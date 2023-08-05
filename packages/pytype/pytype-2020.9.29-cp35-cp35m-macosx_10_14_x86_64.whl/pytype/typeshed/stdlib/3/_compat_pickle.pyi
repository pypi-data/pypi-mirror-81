
from typing import Dict, Tuple
import sys

IMPORT_MAPPING: Dict[str, str]
NAME_MAPPING: Dict[Tuple[str, str], Tuple[str, str]]
PYTHON2_EXCEPTIONS: Tuple[str, ...]
MULTIPROCESSING_EXCEPTIONS: Tuple[str, ...]
REVERSE_IMPORT_MAPPING: Dict[str, str]
REVERSE_NAME_MAPPING: Dict[Tuple[str, str], Tuple[str, str]]
PYTHON3_OSERROR_EXCEPTIONS: Tuple[str, ...]

if sys.version_info >= (3, 6):
    PYTHON3_IMPORTERROR_EXCEPTIONS: Tuple[str, ...]
