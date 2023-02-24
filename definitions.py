import os
from pathlib import Path

from tests_integration import img

PATH_TO_ROOT = os.path.dirname(__file__)
PATH_TO_CREDENTIALS = os.path.join(PATH_TO_ROOT, 'credentials.json')

PATH_TO_TESTS_INTEGRATION_IMG = os.path.join(Path(img.__file__).parent)

