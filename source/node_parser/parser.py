from __future__ import annotations
from enum import Enum
from typing import Union, Optional
from node_parser.tokenizer import Tokenizer, UnexpectedToken

class Tokens(Enum):
    NAME_TOKEN = r'[a-zA-Z_][a-zA-Z_0-9]*'
    EQ_TOKEN = r'='
    VALUE_TOKEN = r'"[^"\n]+"'
    LEFT_BRACE_TOKEN = r'\{'
    RIGHT_BRACE_TOKEN = r'\}'


class Node:
    counter: int = 0

    def __init__(self, parent_id: int = 0, name: str = '',
                  value: Optional[Union[str, list[Node]]] = None):
        self.parent_id = parent_id
        self.name = name
        self.value = value
        Node.counter += 1
        self.id = Node.counter


    def __str__(self, level = 0):
        res = f'{'  '*level}({self.id}, {self.parent_id}, {self.name}, '
        match self.value:
            case list():
                res +=  ' '.join([str(node.id) for node in self.value]) + ')\n'
                for child in self.value:
                    res += child.__str__(level+1)
            case str():
                res += self.value[1:-1] + ')\n'
        return res


class Parser:
    def __init__(self, text: str, include_spaces: bool = False):
        self.tokenizer = Tokenizer(text, include_spaces)
    

    def parse(self):
        node = self.parse_node()
        if self.tokenizer.is_tokens_left():
            raise UnexpectedToken()
        return node
 

    def parse_node(self, parent_id: int = 0):
        
        name = self.tokenizer.consume(Tokens.NAME_TOKEN.value)
        self.tokenizer.consume(Tokens.EQ_TOKEN.value)
        cur_node = Node(parent_id, name)

        next_token = self.tokenizer.look_up([Tokens.LEFT_BRACE_TOKEN.value, Tokens.VALUE_TOKEN.value])
        match next_token:
            case Tokens.LEFT_BRACE_TOKEN.value:
                cur_node.value = self.parse_list(cur_node.id)
            case Tokens.VALUE_TOKEN.value:
                cur_node.value = self.parse_value()
            
        return cur_node
       

    def parse_list(self, parent_id: int):
        node_list = []

        self.tokenizer.consume(Tokens.LEFT_BRACE_TOKEN.value)
        node_list += [self.parse_node(parent_id)]
        while self.tokenizer.look_up([token.value for token in Tokens]) != Tokens.RIGHT_BRACE_TOKEN.value:
            node_list += [self.parse_node(parent_id)]
        self.tokenizer.consume(Tokens.RIGHT_BRACE_TOKEN.value)

        return node_list


    def parse_value(self):
        return self.tokenizer.consume(Tokens.VALUE_TOKEN.value)




            
            


    