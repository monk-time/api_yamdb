from pathlib import Path

from tests.conftest import BASE_DIR, MANAGE_PATH

api_path = MANAGE_PATH / 'api'
if api_path.exists() and api_path.is_dir():
    assert not (api_path / 'models.py').exists(), (
        f'В директории `{api_path}` не должно быть файла с моделями. '
        'В этом приложении они не нужны.'
    )
else:
    msg = f'Не найдено приложение `api` в папке {MANAGE_PATH}'
    raise AssertionError(msg)


# test .md
default_md = '# api_yamdb\napi_yamdb\n'
filename = 'README.md'
assert (BASE_DIR / filename).is_file(), (
    f'В корне проекта не найден файл `{filename}`'
)

file = Path(filename).read_text(encoding='utf-8', errors='ignore')
assert file != default_md, f'Не забудьте оформить `{filename}`'
