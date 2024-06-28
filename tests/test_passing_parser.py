import pytest
from node_parser.parser import Parser, Node

@pytest.fixture(autouse=True)
def reset_Node_counter():
    Node.counter = 0

def test_parse_node_simple_value():
    text = 'name = "value" '
    parser = Parser(text)
    result = parser.parse()
    
    assert isinstance(result, Node)
    assert result.id == 1
    assert result.parent.id == 0
    assert result.name == 'name'
    assert result.value == '"value"'

def test_parse_node_nested_list():
    text = 'parent = {child1 ="value1" child2= "value2"}'
    parser = Parser(text)
    result = parser.parse()
    
    assert isinstance(result, Node)
    assert result.id == 1
    assert result.parent.id == 0
    assert result.name == 'parent'
    assert isinstance(result.value, list)
    assert len(result.value) == 2
    
    child1, child2 = result.value
    assert child1.id == 2
    assert child1.parent.id == result.id
    assert child1.name == 'child1'
    assert child1.value == '"value1"'
    
    assert child2.id == 3
    assert child2.parent.id == result.id
    assert child2.name == 'child2'
    assert child2.value == '"value2"'


def test_parse_node_deep_nesting():
    text = 'root=\n{level1= \n{level2={  level3="deep"}}}'
    parser = Parser(text)
    result = parser.parse()
    
    assert isinstance(result, Node)
    assert result.id == 1
    assert result.parent.id == 0
    assert result.name == 'root'
    assert isinstance(result.value, list)
    assert len(result.value) == 1
    
    level1 = result.value[0]
    assert level1.id == 2
    assert level1.parent.id == 1
    assert level1.name == 'level1'
    assert isinstance(level1.value, list)
    assert len(level1.value) == 1
    
    level2 = level1.value[0]
    assert level2.id == 3
    assert level2.parent.id == 2
    assert level2.name == 'level2'
    assert isinstance(level2.value, list)
    assert len(level2.value) == 1
    
    level3 = level2.value[0]
    assert level3.id == 4
    assert level3.parent.id == 3
    assert level3.name == 'level3'
    assert level3.value == '"deep"'


def test_parse_node_multiple_nested():
    text = 'root\n=\n{child1\n=   {grandchild1=\n"value1"} child2="value2"\n }'
    parser = Parser(text)
    result = parser.parse()
    
    assert isinstance(result, Node)
    assert result.id == 1
    assert result.parent.id == 0
    assert result.name == 'root'
    assert isinstance(result.value, list)
    assert len(result.value) == 2
    
    child1, child2 = result.value
    assert child1.id == 2
    assert child1.parent.id == 1
    assert child1.name == 'child1'
    assert isinstance(child1.value, list)
    assert len(child1.value) == 1
    
    grandchild1 = child1.value[0]
    assert grandchild1.id == 3
    assert grandchild1.parent.id == 2
    assert grandchild1.name == 'grandchild1'
    assert grandchild1.value == '"value1"'
    
    assert child2.id == 4
    assert child2.parent.id == 1
    assert child2.name == 'child2'
    assert child2.value == '"value2"'