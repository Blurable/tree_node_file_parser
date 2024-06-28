import pytest
from node_parser.tokenizer import Tokenizer, UnexpectedToken
from node_parser.parser import Tokens


@pytest.mark.parametrize("test_string, expected_match, expected_result, expected_text_position", [
                        ('_asd=', Tokens.NAME_TOKEN.value, '_asd', 4),
                        ('=asd', Tokens.EQ_TOKEN.value, '=', 1),
                        ('"asd"', Tokens.VALUE_TOKEN.value, '"asd"', 5),
                        ('{asd}', Tokens.LEFT_BRACE_TOKEN.value, '{', 1),
                        ('}asd{', Tokens.RIGHT_BRACE_TOKEN.value, '}', 1)
                        ])

def test_passing_consume(test_string, expected_match, expected_result, expected_text_position):
    tokenizer_instance = Tokenizer(test_string)

    assert tokenizer_instance.consume(expected_match) == expected_result
    assert tokenizer_instance.text_position == expected_text_position
    assert tokenizer_instance.text_position == len(expected_result)


@pytest.mark.parametrize("test_string, expected_match, expected_error", [
                        ('1_asd=', Tokens.NAME_TOKEN.value, UnexpectedToken),
                        ('-', Tokens.EQ_TOKEN.value, UnexpectedToken),
                        ('"""', Tokens.VALUE_TOKEN.value, UnexpectedToken),
                        ('(asd}', Tokens.LEFT_BRACE_TOKEN.value, UnexpectedToken),
                        (')asd{', Tokens.RIGHT_BRACE_TOKEN.value, UnexpectedToken),
                        ('""', Tokens.VALUE_TOKEN.value, UnexpectedToken)
                        ])
def test_failing_consume(test_string, expected_match, expected_error):
    tokenizer_instance = Tokenizer(test_string)

    with pytest.raises(expected_error):
        tokenizer_instance.consume(expected_match)
    assert tokenizer_instance.text_position == 0