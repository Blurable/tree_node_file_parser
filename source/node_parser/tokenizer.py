import re


class UnexpectedToken(Exception):
    def __init__(self, token: str = '', text_position: int = 0, text: str = ''):
        if token:
            self.message = f"\033[91m{token} didn't match with the text. Position = {text_position}, Token = {text[text_position]}.\033[0m"
        else:
            self.message = f"\033[91mExcess text.\033[0m"
        super().__init__(self.message)


class UnexpectedEndOfTextError(Exception):
    def __init__(self):
        self.message = f"\033[91mText has ended.\033[0m"
        super().__init__(self.message)


class Tokenizer:
    def __init__(self, text: str, include_spaces: bool = False):
        self.include_spaces = include_spaces
        self.text = text
        if include_spaces is False:
            self.text = self.text.strip()
        self.text_position = 0
        

    def skip_spaces(self):
        space_pattern = re.compile(r'[\s]*')
        space = space_pattern.match(self.text, self.text_position)
        if space:
            self.text_position += len(space.group())

    
    def is_tokens_left(self):
        return self.text_position < len(self.text)
    

    def look_up(self, patterns: list[str]):
        if self.include_spaces is False:
            self.skip_spaces()
        if self.is_tokens_left() is False:
            raise UnexpectedEndOfTextError

        for pattern in patterns:
            cur_pattern = re.compile(pattern)
            if cur_pattern.match(self.text, self.text_position):
                return pattern
        raise UnexpectedToken('Tokens', self.text_position, self.text)
    

    def consume(self, pattern: str):
        if self.include_spaces is False:
            self.skip_spaces()
        if self.is_tokens_left() is False:
            raise UnexpectedEndOfTextError

        cur_pattern = re.compile(pattern)
        cur_text = cur_pattern.match(self.text, self.text_position)
        if cur_text:
            self.text_position += len(cur_text.group())
            return cur_text.group()
        raise UnexpectedToken(pattern, self.text_position, self.text)