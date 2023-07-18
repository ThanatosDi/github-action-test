import os
import re

import opencc


def is_traditional(text: str) -> bool:
    converter = opencc.OpenCC('s2t.json')
    return text == converter.convert(text)


def main():
    CODE_LANGUAGE = os.environ.get('INPUT_CODE_LANGUAGE', 'python')
    LANGUAGE = os.environ.get('INPUT_LANGUAGE', 'zh-TW')
    print(f'CODE_LANGUAGE: {CODE_LANGUAGE}')
    print(f'LANGUAGE: {LANGUAGE}')


with open('tests/test.php', 'r', encoding='utf-8') as f:
    content = f.read()
PHP_BLOCK_COMMENT = re.compile(r'/\*\*.+?\*/', re.DOTALL)
PHP_ONE_LINE_COMMENT = re.compile(r"//.*")

comments = re.findall(PHP_BLOCK_COMMENT, content) + \
    re.findall(PHP_ONE_LINE_COMMENT, content)

ERROR_COMMENTS = []
for comment in comments:
    if is_traditional(comment) == False:
        ERROR_COMMENTS.append(comment)

test = '// 這是一個範例的類別 汉字'

print(is_traditional(test))

if __name__ == '__main__':
    main()
