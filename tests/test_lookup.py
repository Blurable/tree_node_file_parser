import pytest
from node_parser.tokenizer import Tokenizer, UnexpectedToken
from node_parser.parser import Tokens

@pytest.mark.parametrize("test_string, expected_match", [
                        ('_asd=', Tokens.NAME_TOKEN.value),
                        ('=asd', Tokens.EQ_TOKEN.value),
                        ('"   asd    "', Tokens.VALUE_TOKEN.value),
                        ('{asd}', Tokens.LEFT_BRACE_TOKEN.value),
                        ('}asd{', Tokens.RIGHT_BRACE_TOKEN.value),
                        ('"asd"', Tokens.VALUE_TOKEN.value)
                        ])
def test_positive_lookup(test_string, expected_match):
    list_of_tokens = [token.value for token in Tokens]
    tokenizer_instance = Tokenizer(test_string)
    assert tokenizer_instance.look_up(list_of_tokens) == expected_match


@pytest.mark.parametrize("test_string, expected_result", [
                        ('1_asd', UnexpectedToken),
                        ('*', UnexpectedToken),
                        ('"""', UnexpectedToken)
                        ])
def test_negative_lookup(test_string, expected_result):
    list_of_tokens = [token.value for token in Tokens]
    tokenizer_instance = Tokenizer(test_string)
    with pytest.raises(expected_result):
        tokenizer_instance.look_up(list_of_tokens)


    