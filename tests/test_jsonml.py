from xml.etree import ElementTree

import pytest

from jsonml import Parser


@pytest.fixture(scope="session")
def parser():
    return Parser()


def test_parser_mapping(parser: Parser):
    assert len(parser.mapping) == 1
    assert parser.mapping["node"] is ElementTree.Element


def test_from_jsonml(parser: Parser):
    obj = ["tag1", ["tag2", ["tag3", "1"]]]
    tree1 = parser.parse_from_obj(obj)
    assert isinstance(tree1, ElementTree.Element)
    assert tree1.tag == "tag1"
    assert len(tree1) == 1
    assert tree1.text is None

    tree2 = tree1[0]
    assert isinstance(tree1, ElementTree.Element)
    assert tree2.tag == "tag2"
    assert len(tree2) == 1
    assert tree2.text is None

    tree3 = tree2[0]
    assert isinstance(tree1, ElementTree.Element)
    assert tree3.tag == "tag3"
    assert len(tree3) == 0
    assert tree3.text == "1"


def test_to_jsonml(parser: Parser):
    obj = ["tag1", ["tag2", ["tag3", "1"]]]
    tree = parser.parse_from_obj(obj)
    assert parser.to_jsonml(tree) == obj


def test_from_xml_string(parser: Parser):
    obj = ["tag1", ["tag2", ["tag3", "1"]]]
    tree = parser.parse_from_obj(obj)
    xml = parser.to_xml(tree)
    tree2 = parser.parse_from_xml_string(xml)
    assert parser.to_jsonml(tree2) == obj
