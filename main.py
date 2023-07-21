import json
import os
import sys

import zhconv
from alive_progress import alive_it

from modules.php import PHP
# from modules.python import Python


def is_traditional(text: str, custom_dictionary: dict = {}) -> bool:
    with open('./dictionary.json', 'r', encoding='utf-8') as f:
        dictionary = json.loads(f.read())
    dictionary.update(custom_dictionary)
    traditional_text = zhconv.convert(text, 'zh-tw', dictionary)
    return traditional_text == text


def suggestion(text: str, custom_dictionary: dict = {}) -> str:
    with open('./dictionary.json', 'r', encoding='utf-8') as f:
        dictionary = json.loads(f.read())
    dictionary.update(custom_dictionary)
    traditional_text = zhconv.convert(text, 'zh-tw', dictionary)
    return traditional_text


def main():
    CODE_LANGUAGE = os.environ.get('code-language', 'php')
    ROOT_PATH = os.environ.get('root-path', './')  # TODO: 正式時要修改路徑為 ../
    CUSTOM_DICTIONARY = json.loads(os.environ.get('custom-dictionary', "{}").replace('\'', '"'))
    SCAN_DIR = os.environ.get(
        'scan-dir', 'tests, app').replace(' ', '').split(',')
    ERROR_COMMENTS = []

    files = PHP().files(path=ROOT_PATH, include_dir=SCAN_DIR)
    comments = []
    for file in alive_it(files):
        match(CODE_LANGUAGE.lower()):
            case 'php':
                comments = PHP().comments(file)
            # TODO: Python 語言的實現
            case _:
                raise ValueError('Not support this language')
        for comment in comments:
            if not is_traditional(comment, custom_dictionary=CUSTOM_DICTIONARY):
                ERROR_COMMENTS.append({os.path.basename(file): comment})
    if any(ERROR_COMMENTS):
        print(f"::group::發現錯誤")  # NOSONAR
        for comment in ERROR_COMMENTS:
            for filename, comment in comment.items():
                print(
                    f"::error file={filename}:: {filename}: {comment} ({suggestion(comment)})")
        print(f"::endgroup::")  # NOSONAR
        sys.exit(1)


if __name__ == '__main__':
    main()
