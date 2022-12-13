import re


def format_latin_words(s: str) -> str:
    """Use a regular expression to match any Latin words in the input string"""
    pattern = re.compile(r'\b(?!\d*[.-]|[.-]*\d)[a-zA-Z0-9]+\b')
    return pattern.sub(lambda m: '`' + m.group(0) + '`', s)


def replace_arrows(s: str) -> str:
    return s.replace('->', ' ➡️')


def replace_newlines(s: str) -> str:
    return s.replace('\n', '\\n')


def surround_with_quotes(s: str) -> str:
    return '"' + s + '"'


test = "*Необходимо подключение к интернету!*\n\n➡️ Нажмите пуск, далее параметры\n➡️ Система и самое нижнее в левом боковом меню о программе\n➡️ Раздел характеристики `Windows`, смотрим версия\n22H2 последняя версия  `Win10`/11\n➡️ Возвращаемся в параметры, обновление и безопастность\n➡️ Центр обновления `Windows`, проверить наличие обновлений\n\nИли\n➡️ Скачать программу помощник обновлений и запустить\n Ссылка на скачивание ...........\n➡️ Дождаться окончания загрузки и установки\n"



if __name__ == "__main__":
    # Open the file in read mode
    with open('test.txt', 'r') as file:
        # Read the contents of the file
        contents = file.read()

    contents = format_latin_words(contents)
    contents = replace_arrows(contents)
    contents = replace_newlines(contents)
    contents = surround_with_quotes(contents)

    print(contents)
