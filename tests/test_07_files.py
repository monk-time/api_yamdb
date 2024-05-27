import os
from pathlib import Path

from tests.conftest import MANAGE_PATH, project_dir_content, root_dir_content

api_path = MANAGE_PATH / 'api'
if 'api' in project_dir_content and api_path.is_dir():
    api_dir_content = os.listdir(api_path)
    assert 'models.py' not in api_dir_content, (
        f'В директории `{api_path}` не должно быть файла с моделями. '
        'В этом приложении они не нужны.'
    )
else:
    msg = f'Не найдено приложение `api` в папке {MANAGE_PATH}'
    raise AssertionError(msg)


# test .md
default_md = '# api_yamdb\napi_yamdb\n'
filename = 'README.md'
assert (
    filename in root_dir_content
), f'В корне проекта не найден файл `{filename}`'

file = Path(filename).read_text(encoding='utf-8', errors='ignore')
assert file != default_md, f'Не забудьте оформить `{filename}`'
