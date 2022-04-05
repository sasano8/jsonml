from xml.etree import ElementTree


def to_xml(element: ElementTree.Element, as_byte: bool = False):
    if as_byte:
        return ElementTree.tostring(element)
    else:
        return ElementTree.tostring(element).decode("utf8")


def to_jsonml(element: ElementTree.Element):
    tag = element.tag
    attrib = element.attrib
    text = element.text
    children = [to_jsonml(x) for x in element]

    result = [tag]
    if len(attrib) != 0:
        result.append(attrib)  # type: ignore

    if text is not None:
        result.append(text)

    for child in children:
        result.append(child)

    return result
