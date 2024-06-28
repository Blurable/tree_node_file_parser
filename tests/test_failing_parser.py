import pytest
from node_parser.parser import Parser
from node_parser.tokenizer import UnexpectedToken, UnexpectedEndOfTextError


@pytest.mark.parametrize("text, expected_error", [
                        ('root={}', UnexpectedToken),
                        ('1root="value"  ', UnexpectedToken),
                        ('root={child1}', UnexpectedToken),
                        ('root=="value"', UnexpectedToken),
                        ('root={"value"} ', UnexpectedToken),
                        ('root={child1={grandchild1="value"}', UnexpectedEndOfTextError),
                        ('root=', UnexpectedEndOfTextError),
                        ('"value"', UnexpectedToken),
                        ('root{}', UnexpectedToken),
                        ('=root{}', UnexpectedToken),
                        ('root="val"ue=""', UnexpectedToken),
                        ('', UnexpectedEndOfTextError),
                        (' ', UnexpectedEndOfTextError),
                        ('root="""', UnexpectedToken),
                        ('root}', UnexpectedToken),
                        ('root = {child1="abc"}root2="value"', UnexpectedToken),
                        ('root={child1="value"', UnexpectedEndOfTextError)
                        ])
def test_failing_parser_no_spaces(text, expected_error):
    parser = Parser(text)

    with pytest.raises(expected_error):
        parser.parse()


@pytest.mark.parametrize("text, expected_error", [
                        ('parent = {child1 ="value1" child2= "value2"}', UnexpectedToken),
                        ('name = "value"', UnexpectedToken),
                        ('root=\n{level1= \n{level2={  level3="deep"}}}', UnexpectedToken),
                        ('root\n=\n{child1\n=   {grandchild1=\n"value1"} child2="value2"\n }', UnexpectedToken),
                        ])
def test_failing_parser_with_spaces(text, expected_error):
    parser = Parser(text, True)

    with pytest.raises(expected_error):
        parser.parse()



