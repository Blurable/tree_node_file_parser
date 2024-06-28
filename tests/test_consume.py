import pytest
from node_parser.tokenizer import Tokenizer, UnexpectedToken
from node_parser.parser import Tokens


@pytest.mark.parametrize("test_string, expected_match, expected_result", [
                        ('_asd=', Tokens.NAME_TOKEN.value, '_asd'),
                        ('=asd', Tokens.EQ_TOKEN.value, '='),
                        ('"asd"', Tokens.VALUE_TOKEN.value, '"asd"'),
                        ('{asd}', Tokens.LEFT_BRACE_TOKEN.value, '{'),
                        ('}asd{', Tokens.RIGHT_BRACE_TOKEN.value, '}'),
                        ('_123', Tokens.NAME_TOKEN.value, '_123'),
                        ('_a1a1a1', Tokens.NAME_TOKEN.value, '_a1a1a1'),
                        ('_1111a', Tokens.NAME_TOKEN.value, '_1111a'),
                        ('" "', Tokens.VALUE_TOKEN.value, '" "')
                        ])

def test_passing_consume(test_string, expected_match, expected_result):
    tokenizer_instance = Tokenizer(test_string)

    assert tokenizer_instance.consume(expected_match) == expected_result
    assert tokenizer_instance.cursor == len(expected_result)


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
    assert tokenizer_instance.cursor == 0