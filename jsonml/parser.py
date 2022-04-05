import copy
import inspect
from typing import Callable, Type, Union
from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser as _XMLParser

from .exporter import to_jsonml, to_xml


class Undefined:
    ...


Undefined = Undefined()  # type: ignore


def build_selector(
    mapping: dict = None,
    default: Union[str, None, Type[ElementTree.Element]] = ElementTree.Element,
) -> Callable[[str], Type[ElementTree.Element]]:

    mapping: dict = mapping or {}

    if not isinstance(mapping, dict):
        raise TypeError()

    if isinstance(default, str):
        default = mapping[default]

    if inspect.isclass(default) and issubclass(default, ElementTree.Element):

        def selector(tag: str) -> Type[ElementTree.Element]:
            try:
                return mapping[tag.lower()]
            except KeyError:
                return default

    elif default is None:

        def selector(tag: str) -> Type[ElementTree.Element]:
            return mapping[tag.lower()]

    else:
        raise TypeError()

    return selector


class BaseXMLParser:
    def __init__(
        self,
        selector: Union[dict, Callable] = None,
    ):
        if selector is None:
            selector = build_selector()

        if isinstance(selector, dict):
            selector = selector.__getitem__

        self.selector: Callable[[str], Type[ElementTree.Element]] = selector

    def create_element(self, tag: str, attrs) -> ElementTree.Element:
        factory = self.selector(tag)
        return factory(tag, attrs)

    def parse_from_xml_string(self, xml: str, encoding=None):
        tb = ElementTree.TreeBuilder(element_factory=self.create_element)
        parser = _XMLParser(target=tb, encoding=None)
        return ElementTree.fromstring(
            xml,
            parser=parser,
        )

    def to_xml(self, element: ElementTree.Element, as_byte: bool = False):
        return to_xml(element, as_byte)

    def to_jsonml(self, element: ElementTree.Element):
        return to_jsonml(element)


class JsonMLParser(BaseXMLParser):
    def parse(self, obj: list, deepcopy: bool = True):
        if not isinstance(obj, list):
            raise TypeError()

        obj = copy.deepcopy(obj)

        it = iter(obj)

        tag = next(it)
        attrib = Undefined
        children = []
        texts = []

        if not isinstance(tag, str):
            raise TypeError()

        for item in it:
            if isinstance(item, list):
                children.append(self.parse(item))
            elif isinstance(item, str):
                texts.append(item)
            elif isinstance(item, dict):
                if attrib is Undefined:
                    attrib = item
                else:
                    raise RuntimeError("１度だけ設定可能")
            else:
                raise TypeError()

        if attrib is Undefined:
            attrib = {}

        elm = self.create_element(tag, attrib)
        elm.extend(children)

        if texts:
            elm.text = " ".join(texts)

        return elm
