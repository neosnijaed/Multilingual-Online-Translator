import argparse
from translator_class import LanguageTranslator
from translator_exception import InvalidWord, InvalidLanguage


def take_command_line_arguments() -> tuple[str, str, str]:
    """
    Parses command-line arguments to obtain the source language, target language, and the word to be translated.

    Returns:
        - Tuple[str, str, str] with the user's language, the desired translation language and the word to be translated.
    """
    parser = argparse.ArgumentParser(description='Multilingual Online Translator')
    parser.add_argument('source_language', help='User\'s language')
    parser.add_argument('target_language', help='Translation language')
    parser.add_argument('word', help='Word to be translated')
    args = parser.parse_args()
    return args.source_language, args.target_language, args.word


def select_users_language(language: str, translator: LanguageTranslator) -> None:
    """
    Validates the source language and sets it in the LanguageTranslator instance.

    Params:
        - language (str): The source language.
        - translator (LanguageTranslator): The LanguageTranslator instance.
    """
    if not language.isalpha():
        raise InvalidWord(language)
    if not language.title() in translator.languages:
        raise InvalidLanguage(language.title())
    translator.translate_from = language.lower()


def select_translation_language(language: str, translator: LanguageTranslator) -> None:
    """
    Validates the target language and sets it in the LanguageTranslator instance.

    Params:
        - language (str): The target language.
        - translator (LanguageTranslator): The LanguageTranslator instance.
    :return:
    """
    try:
        if not language.isalpha():
            raise InvalidWord(language)
        if language.title() not in translator.languages and language.lower() != 'all':
            raise InvalidLanguage(language.title())
    except (InvalidWord, InvalidLanguage) as err:
        print(err)
        exit(1)
    translator.translate_to = language.lower()


def get_word_to_translate(word: str, translator: LanguageTranslator) -> None:
    """
    Validates the word and sets it in the LanguageTranslator instance.

    Params:
        - word (str): The word to be translated.
        - translator (LanguageTranslator): The LanguageTranslator instance.
    """
    if not word.isalpha():
        raise InvalidWord(word)
    translator.word = word.lower()


def main() -> None:
    """The main function that orchestrates the translation process."""

    source_language, target_language, word = take_command_line_arguments()
    translator = LanguageTranslator()
    select_users_language(source_language, translator)
    select_translation_language(target_language, translator)
    get_word_to_translate(word, translator)
    if translator.translate_to == 'all':
        translator.languages.remove(translator.translate_from.title())
        for language in translator.languages:
            translator.translate_to = language.lower()
            response = translator.fetch_webpage_response()
            parser = translator.parse_webpage_response(response)
            translator.display_and_save_all_translations(parser)
    else:
        response = translator.fetch_webpage_response()
        parser = translator.parse_webpage_response(response)
        translator.display_and_save_translations(parser)


if __name__ == '__main__':
    main()
