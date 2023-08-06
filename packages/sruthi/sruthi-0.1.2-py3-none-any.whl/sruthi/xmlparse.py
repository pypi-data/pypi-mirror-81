import re
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as etree
import xmltodict
from . import errors


class XMLNone(object):
    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    def iter(self):
        return []

    text = None


class XMLParser(object):
    def __init__(self):
        self.namespaces = {
            'sru': 'http://www.loc.gov/zing/srw/',
            'isad': 'http://www.expertisecentrumdavid.be/xmlschemas/isad.xsd',
            'rel': 'info:srw/extension/2/relevancy-1.0',
            'ap': 'http://www.archivportal.ch/srw/extension/',
            'zr': 'http://explain.z3950.org/dtd/2.1/',
        }
        self.dict_namespaces = {
            'http://www.loc.gov/zing/srw/': 'sru',
            'http://explain.z3950.org/dtd/2.1/': 'zr',
            'info:srw/extension/2/relevancy-1.0': None,
            'http://www.archivportal.ch/srw/extension/': None,
            'http://www.loc.gov/MARC21/slim': None,
            'http://www.loc.gov/mods/v3': None,
            'http://www.loc.gov/standards/mods/v3/mods-3-6.xsd': None,
            'http://www.loc.gov/standards/mods/v3/mods-3-6.xsd': None,
            'http://purl.org/dc/elements/1.1/': None,
            'http://www.expertisecentrumdavid.be/xmlschemas/isad.xsd': None,
            'http://www.w3.org/2001/XMLSchema-instance': None,
            'http://www.w3.org/XML/1998/namespace': None,
        }

    def parse(self, content):
        try:
            return etree.fromstring(content)
        except Exception as e:
            raise errors.SruError("Error while parsing XML: %s" % e)

    def find(self, xml, path):
        if isinstance(path, list):
            for p in path:
                elem = self.find(xml, p)
                if not isinstance(elem, XMLNone):
                    return elem
            return XMLNone()
        elem = xml.find(path, self.namespaces)
        if elem is None:
            return XMLNone()
        return elem

    def findall(self, xml, path):
        return xml.findall(path, self.namespaces)

    def tostring(self, xml):
        return etree.tostring(xml)

    def todict(self, xml, **kwargs):
        if isinstance(xml, XMLNone):
            return None
        if isinstance(xml, Element):
            xml = self.tostring(xml)

        dict_args = {
            'dict_constructor': dict,
            'process_namespaces': True,
            'namespaces': self.dict_namespaces,
            'attr_prefix': '',
            'cdata_key': 'text',
        }
        dict_args.update(kwargs)
        return dict(xmltodict.parse(xml, **dict_args))

    def namespace(self, element):
        m = re.match(r'\{(.*)\}', element.tag)
        return m.group(1) if m else ''
