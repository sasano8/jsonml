from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser as _XMLParser


class Undefined:
    ...


Undefined = Undefined()  # type: ignore


class JsonMLParser:
    def __init__(
        self, mapping: dict = {"node": ElementTree.Element}, default_cls: str = "node"
    ):
        default = mapping.get(default_cls)

        def selector(tag: str):
            return mapping.get(tag.lower(), default)

        self.mapping = mapping
        self.selector = selector

    def create_element(self, tag: str, attrs) -> ElementTree.Element:
        factory = self.selector(tag)
        return factory(tag, attrs)

    def to_xml(self, element: ElementTree.Element, as_byte: bool = False):
        if as_byte:
            return ElementTree.tostring(element)
        else:
            return ElementTree.tostring(element).decode("utf8")

    def to_jsonml(self, element: ElementTree.Element):
        tag = element.tag
        attrib = element.attrib
        text = element.text
        children = [self.to_jsonml(x) for x in element]

        result = [tag]
        if len(attrib) != 0:
            result.append(attrib)  # type: ignore

        if text is not None:
            result.append(text)

        for child in children:
            result.append(child)

        return result

    def parse_from_xml_string(self, xml: str, encoding=None):
        tb = ElementTree.TreeBuilder(element_factory=self.create_element)
        parser = _XMLParser(target=tb, encoding=None)
        return ElementTree.fromstring(
            xml,
            parser=parser,
        )

    def parse_from_obj(self, obj):
        if not isinstance(obj, list):
            raise TypeError()

        it = iter(obj)

        tag = next(it)
        attrib = Undefined
        children = []
        texts = []

        if not isinstance(tag, str):
            raise TypeError()

        for item in it:
            if isinstance(item, list):
                children.append(self.parse_from_obj(item))
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
