import os
import re

import opencc

from modules.php import PHP
from modules.python import Python


def is_traditional(text: str) -> bool:
    converter = opencc.OpenCC('s2t.json')
    return text == converter.convert(text)


def main():
    CODE_LANGUAGE = os.environ.get('code-language', 'python')
    LANGUAGE = os.environ.get('comment-language', 'zh-TW')
    print(f'CODE_LANGUAGE: {CODE_LANGUAGE}')
    print(f'LANGUAGE: {LANGUAGE}')


# comments = PHP().comments('tests/test.php')

# ERROR_COMMENTS = []
# for comment in comments:
#     if is_traditional(comment) == False:
#         ERROR_COMMENTS.append(comment)

# test = '// 這是一個範例的類別 汉字'

# print(is_traditional(test))

if __name__ == '__main__':
    main()
