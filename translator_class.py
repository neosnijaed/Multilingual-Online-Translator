import os

import requests
from bs4 import BeautifulSoup

from translator_exception import WebsiteConnectionError, InvalidWord


class LanguageTranslator:
    """This class facilitates the translation of words between various languages using the Reverso Context
    translation service."""

    def __init__(self):
        """
        Initializer of the LanguageTranslator class.

        Attributes:
            - word (str): The word to be translated.
            - translate_from (str): The source language for the translation.
            - translate_to (str): The target language for the translation.
            - languages (list[str]): List of supported languages.
        """
        self.word = ''
        self.translate_from = ''
        self.translate_to = ''
        self.languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
                          'Portuguese', 'Romanian', 'Russian', 'Turkish']

    def fetch_webpage_response(self) -> requests.Response:
        """
        Fetches the webpage containing the translation for the given word from the Reverso Context service.

        Returns:
            - response (request.Response): Instance with HTML content.
        """
        headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
        response = requests.get(
            f'https://context.reverso.net/translation/{self.translate_from}-{self.translate_to}/{self.word}',
            headers=headers
        )
        try:
            if not response:
                raise InvalidWord(self.word)
        except InvalidWord as err:
            print(err)
            exit(1)
        try:
            if response.status_code == '404':
                raise WebsiteConnectionError
        except InvalidWord as err:
            print(err)
            exit(1)
        return response

    @staticmethod
    def parse_webpage_response(response: requests.Response) -> BeautifulSoup:
        """
        Parses the HTML content of the webpage response using BeautifulSoup.

        Params:
            - response (request.Response): Instance with HTML content.

        Returns:
            - BeautifulSoup instance with parsed HTML content.
        """
        return BeautifulSoup(response.content, 'html.parser')

    def display_and_save_translations(self, soup: BeautifulSoup) -> None:
        """
        Extracts translations and examples from the parsed HTML document and saves them to a file.
        It then displays the content of the file.

        Params:
            - soup (BeautifulSoup): BeautifulSoup instance with parsed HTML content.
        """
        translations = [
            translation.text for translation in soup.select('#translations-content .translation .display-term')
        ]
        examples_from = [example.text.strip() for example in soup.select('.example .src .text')]
        examples_to = [example.text.strip() + '\n' for example in soup.select('.example .trg .text')]
        self.save_to_file(translations, examples_from, examples_to)
        self.display_file_content()

    def display_and_save_all_translations(self, soup: BeautifulSoup) -> None:
        """
        Extracts translations and corresponding examples from the parsed HTML document,
        regardless of the specified target language. Saves this information to a file and displays the content.

        Params:
            - soup (BeautifulSoup): BeautifulSoup instance with parsed HTML content.
        """
        translation = soup.select_one('#translations-content .display-term').text.strip()
        example_from = soup.select_one('.example .src .text').text.strip()
        example_to = soup.select_one('.example .trg .text').text.strip()
        self.save_to_file([translation], [example_from], [example_to])
        self.display_file_content()

    def save_to_file(self, translations: list, examples_from: list, examples_to: list) -> None:
        """
        Saves the translations and examples to a text file named after the word being translated.

        Params:
            - translations (list[str]): List of translations.
            - examples_from (list[str]): List of source examples.
            - examples_to (list[str]): List of target examples.
        """
        if not os.path.exists(f'{self.word}.txt'):
            open(f'{self.word}.txt', 'w', encoding='utf-8').close()
        with open(f'{self.word}.txt', 'a', encoding='utf-8') as file:
            file.write(f'{self.translate_to.title()} Translations:\n')
            file.write('\n'.join(translations))
            file.write('\n')
            file.write(f'\n{self.translate_to.title()} Examples:\n')
            for ex_from, ex_to in zip(examples_from, examples_to):
                file.write(f'{ex_from}\n{ex_to}\n')
            file.write('\n')

    def display_file_content(self) -> None:
        """
        Displays the content of the file containing the translations and examples.
        """
        with open(f'{self.word}.txt', 'r', encoding='utf-8') as file:
            print(file.read())
