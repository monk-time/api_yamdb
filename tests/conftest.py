import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'api_yamdb'

if (
    PROJECT_DIR_NAME not in root_dir_content
    or not (BASE_DIR / PROJECT_DIR_NAME).is_dir()
):
    msg = (
        f'В директории `{BASE_DIR}` не найдена папка c проектом '
        f'`{PROJECT_DIR_NAME}`. Убедитесь, что у вас верная структура проекта.'
    )
    raise AssertionError(msg)

MANAGE_PATH = BASE_DIR / PROJECT_DIR_NAME
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'

if FILENAME not in project_dir_content:
    msg = (
        f'В директории `{MANAGE_PATH}` не найден файл `{FILENAME}`. '
        'Убедитесь, что у вас верная структура проекта.'
    )
    raise AssertionError(msg)

pytest_plugins = [
    'tests.fixtures.fixture_user',
]
