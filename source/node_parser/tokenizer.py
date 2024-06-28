import re


class UnexpectedToken(Exception):
    def __init__(self, token: str = '', text_position: int = 0, text: str = ''):
        if token:
            self.message = f"\033[91m{token} didn't match with the text. Position = {text_position}, Token = {text[text_position]}.\033[0m"
        else:
            self.message = f"\033[91mUnexpected Token.\033[0m"
        super().__init__(self.message)


class UnexpectedEndOfTextError(Exception):
    def __init__(self):
        self.message = f"\033[91mText has ended.\033[0m"
        super().__init__(self.message)


class Tokenizer:
    def __init__(self, text: str, is_skip_white_space: bool = False):
        self.include_spaces = is_skip_white_space
        self.text = text
        if is_skip_white_space is False:
            self.text = self.text.strip()
        self.cursor = 0
        

    def skip_white_spaces(self):
        space_pattern = re.compile(r'[\s]*')
        space = space_pattern.match(self.text, self.cursor)
        if space:
            self.cursor += len(space.group())

    
    def is_tokens_left(self):
        return self.cursor < len(self.text)
    

    def look_up(self, patterns: list[str]):
        if self.include_spaces is False:
            self.skip_white_spaces()
        if self.is_tokens_left() is False:
            raise UnexpectedEndOfTextError

        for pattern in patterns:
            cur_pattern = re.compile(pattern)
            if cur_pattern.match(self.text, self.cursor):
                return pattern
        raise UnexpectedToken(' '.join(patterns), self.cursor, self.text)
    

    def consume(self, pattern: str):
        if self.include_spaces is False:
            self.skip_white_spaces()
        if self.is_tokens_left() is False:
            raise UnexpectedEndOfTextError

        cur_pattern = re.compile(pattern)
        cur_text = cur_pattern.match(self.text, self.cursor)
        if cur_text:
            self.cursor += len(cur_text.group())
            return cur_text.group()
        raise UnexpectedToken(pattern, self.cursor, self.text)