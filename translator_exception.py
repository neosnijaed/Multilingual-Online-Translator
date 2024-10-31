class InvalidWord(Exception):
    """This exception is raised when an invalid or non-existent word is used in the translation process."""

    def __init__(self, word: str):
        """
        Initializes the InvalidWord exception with the given word.

        Params:
            - word (str): The word that could not be found.
        """
        self.word = word

    def __str__(self):
        """
        Returns the error message indicating that the word could not be found.

        Returns:
            - String for the error message.
        """
        return f'Sorry, unable to find {self.word}'


class WebsiteConnectionError(Exception):
    """
    This exception is raised when there are issues with the internet connection,
    preventing the translation service from fetching the necessary data.
    """

    def __str__(self):
        """
        Returns the error message indicating a problem with the internet connection.

        Returns:
            - String for the error message.
        """
        return 'Something wrong with your internet connection'


class InvalidLanguage(Exception):
    """
    The InvalidLanguage exception is raised when a language that is not supported by the
    translation program is specified.
    """

    def __init__(self, language: str):
        """
        Initializes the InvalidLanguage exception with the given language.

        Params:
            - language (str): The language that is not supported.
        """
        self.language = language

    def __str__(self):
        """
        Returns the error message indicating that the specified language is not supported.

        Returns:
            - String for the error message.
        """
        return f'Sorry, the program doesn\'t support {self.language}'
