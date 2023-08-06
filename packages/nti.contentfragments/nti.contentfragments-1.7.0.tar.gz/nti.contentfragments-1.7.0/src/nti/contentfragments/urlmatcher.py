#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An Improved Liberal, Accurate Regex Pattern for Matching URLs

.. $Id: urlmatcher.py 85352 2016-03-26 19:08:54Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import six

from lxml import etree

from html5lib import HTMLParser
from html5lib import treebuilders

from zope import interface

from nti.contentfragments.interfaces import HTMLContentFragment
from nti.contentfragments.interfaces import IHyperlinkFormatter
from nti.contentfragments.interfaces import IHTMLContentFragment

try:
    unicode
except NameError:
    # Py3
    unicode = str

Element = getattr(etree, 'Element')
etree_tostring = getattr(etree, 'tostring')

# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# https://gist.github.com/gruber/249502

grubber_v1 = \
    (u'((?:[a-z][\\w-]+:(?:/{1,3}|[a-z0-9%])|www\\d{0,3}[.]|[a-z0-9.\\-]+',
     u'[.][a-z]{2,4}/)(?:[^\\s()<>]+|\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\))+',
     u'(?:\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\)|[^\\s`!()\\[\\]{};:\'".,<>?',
     u'\xc2\xab\xc2\xbb\xe2\x80\x9c\xe2\x80\x9d\xe2\x80\x98\xe2\x80\x99]))')

@interface.implementer(IHyperlinkFormatter)
class GrubberHyperlinkFormatter(object):

    grubber_v1_pattern = re.compile(u''.join(grubber_v1))

    def _check_href(self, href):
        if not href.startswith(u'http') and not href.startswith(u'mailto'):
            href = u'http://' + href
        return href

    def _check_text(self, text):
        if text.startswith(u'mailto:'):
            text = text[7:]
        return text

    def find_links(self, text, pattern=grubber_v1_pattern):
        result = []
        m = pattern.search(text)
        while m:
            end = m.end()
            start = m.start()
            result.append(text[0:start])

            href = self._check_href(text[start:end]).strip()
            e = Element('a', href=href)
            e.text = self._check_text(text[start:end])
            result.append(e)

            text = text[end:]
            m = pattern.search(text)

        if text:
            result.append(text)

        return result

    def _a_builder(self, node, pattern, is_text=True):
        field = u'text' if is_text else u'tail'
        text = getattr(node, field, None)
        if text:
            result = self.find_links(text, pattern=pattern)
            setattr(node, field, None)
            for i, e in enumerate(result):
                if isinstance(e, six.string_types):
                    if i == 0:
                        setattr(node, field, e)
                    else:
                        result[i - 1].tail = e
                elif is_text:
                    node.append(e)
                else:
                    parent = node.getparent()
                    if parent is not None:
                        parent.append(e)

    def _link_finder(self, node):
        if node.tag != 'a':
            self._a_builder(node, self.grubber_v1_pattern, True)
        self._a_builder(node, self.grubber_v1_pattern, False)

    def format(self, html_fragment):
        if IHTMLContentFragment.providedBy(html_fragment):
            html_fragment = self._parse_and_linkify(html_fragment,
                                                    html_fragment.__class__)
        elif isinstance(html_fragment, six.string_types) and \
             self.grubber_v1_pattern.search(html_fragment):
            # A plain string that matches
            html_fragment = self._parse_and_linkify(html_fragment, HTMLContentFragment)
        return html_fragment

    def _parse_and_linkify(self, content, dest_class):
        p = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"),
                       namespaceHTMLElements=False)
        doc = p.parse(content)
        for node in doc.iter():
            self._link_finder(node)

        docstr = etree_tostring(doc, encoding=unicode)
        html_fragment = dest_class(docstr)
        return html_fragment
