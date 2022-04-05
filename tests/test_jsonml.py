from xml.etree import ElementTree

import pytest

from jsonml import Parser, build_selector


@pytest.fixture(scope="session")
def parser():
    return Parser()


def test_build_selector():
    class TestElement(ElementTree.Element):
        ...

    with pytest.raises(Exception):
        selector1 = build_selector(
            {"node": ElementTree.Element}, default="not_registerd"
        )

    selector1 = build_selector({"node": ElementTree.Element}, default="node")
    assert selector1("node") is ElementTree.Element
    assert selector1("other") is ElementTree.Element

    selector1 = build_selector(
        {"node": ElementTree.Element, "node2": TestElement}, default="node2"
    )
    assert selector1("node") is ElementTree.Element
    assert selector1("node2") is TestElement
    assert selector1("other") is TestElement

    selector1 = build_selector({"node": ElementTree.Element}, default=None)
    assert selector1("node") is ElementTree.Element

    with pytest.raises(KeyError):
        selector1("other")


def test_default_selector(parser: Parser):
    assert parser.selector("xxx") is ElementTree.Element


def test_from_jsonml(parser: Parser):
    obj = ["tag1", ["tag2", ["tag3", "1"]]]
    tree1 = parser.parse(obj)
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
    tree = parser.parse(obj)
    assert parser.to_jsonml(tree) == obj


def test_from_xml_string(parser: Parser):
    obj = ["tag1", ["tag2", ["tag3", "1"]]]
    tree = parser.parse(obj)
    xml = parser.to_xml(tree)
    tree2 = parser.parse_from_xml_string(xml)
    assert parser.to_jsonml(tree2) == obj
