import abc


class IPythonDiceLexer(abc.ABC):
    @abc.abstractmethod
    def lex(self, input_text: str):
        """

        :return: a list of lexer tokens built from the input text
        """
