import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

PROJECT_DIR_NAME = 'api_yamdb'
MANAGE_PATH = BASE_DIR / PROJECT_DIR_NAME

if not MANAGE_PATH.exists() or not (BASE_DIR / PROJECT_DIR_NAME).is_dir():
    msg = (
        f'В директории `{BASE_DIR}` не найдена папка c проектом '
        f'`{PROJECT_DIR_NAME}`. Убедитесь, что у вас верная структура проекта.'
    )
    raise AssertionError(msg)

FILENAME = 'manage.py'

if not (MANAGE_PATH / FILENAME).is_file():
    msg = (
        f'В директории `{MANAGE_PATH}` не найден файл `{FILENAME}`. '
        'Убедитесь, что у вас верная структура проекта.'
    )
    raise AssertionError(msg)

pytest_plugins = [
    'tests.fixtures.fixture_user',
]
