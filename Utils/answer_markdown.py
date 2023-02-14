import re


def remove_nbsp_char(s: str) -> str:
    return s.replace(' ', '')


def replace_dash(s: str) -> str:
    return s.replace('	', '- ')


def format_latin_words(s: str) -> str:
    """Use a regular expression to match any Latin words in the input string"""
    pattern = re.compile(r'\b(?!\d*[.-]|[.-]*\d)[a-zA-Z0-9]+\b')
    return pattern.sub(lambda m: '`' + m.group(0) + '`', s)


def replace_arrows(s: str) -> str:
    return s.replace('->', ' ➡️')


def replace_newlines(s: str) -> str:
    return s.replace('\n', '\\n')


def bold_titles(s: str) -> str:
    print(s)
    # Find all occurrences of "\n\n" in the input string
    occurrences = [m.start() for m in re.finditer("\n\n", s)]
    print(occurrences)

    # Handle the first occurrence of "\n\n"
    if "\n" not in s[:occurrences[0]]:
        s = "*" + s[:occurrences[0]] + "*" + s[occurrences[0]:]
        occurrences = [i + 2 for i in occurrences]

    # Handle all other occurrences of "\n\n"
    for i in range(2, len(occurrences) - 1):
        start = occurrences[i - 1]
        end = occurrences[i]
        s = s[:start + 2] + "*" + s[start + 2:end] + "*" + s[end:]
        occurrences = [j + 2 for j in occurrences]

    # Handle the last occurrence of "\n\n"
    if "\n" not in s[occurrences[-1] + 2:-1]:
        if s.endswith("\n"):
            s = s[:occurrences[-1] + 2] + "*" + s[occurrences[-1] + 2:-1] + "*"
        else:
            s = s[:occurrences[-1] + 2] + "*" + s[occurrences[-1] + 2:] + "*"

    return s


def surround_with_quotes(s: str) -> str:
    return '"' + s + '"'


test = "*Сброс `SMC` с Т2 и без чипа (Т2 на устройствах от 2017 г.в.)*\n\n- Выключите ваш `Mac`\n- Зажмите одновременно `control` + `shift` + `option`(`alt`)и удерживайте 7 и 10 секунд\n- Не отпуская кнопок пункта 2 нажмите кнопку включения и удерживайте ещё 7 секунд\n- Включите `Mac` обычным способом \n\n*Сброс `NVRAM` на любом `Mac`*\n\n- Выключите ваш `Mac`\n- Зажмите одновременно `option`(`alt`) + `command` + `R` + `P` и удерживайте 15 секунд\n- Не отпуская кнопок пункта 2 нажмите и отпустите кнопку включения\n\n*Могу измениться пользовательские параметры.*"



if __name__ == "__main__":
    # Open the file in read mode
    with open('test.txt', 'r') as file:
        # Read the contents of the file
        contents = file.read()

    contents = remove_nbsp_char(contents)
    contents = replace_dash(contents)
    contents = replace_arrows(contents)
    contents = format_latin_words(contents)
    contents = bold_titles(contents)
    contents = replace_newlines(contents)
    contents = surround_with_quotes(contents)

    print(contents)
