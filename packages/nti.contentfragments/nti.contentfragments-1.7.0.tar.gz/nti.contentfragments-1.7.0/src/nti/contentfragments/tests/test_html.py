#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
__docformat__ = "restructuredtext en"

# pylint:disable=line-too-long


import contextlib

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import same_instance

from zope import component
from zope import interface

from nti.contentfragments.interfaces import IAllowedAttributeProvider

from nti.testing.matchers import verifiably_provides

import os
try:
    from plistlib import load as load_plist
except ImportError:
    from plistlib import readPlist as load_plist

from nti.contentfragments import interfaces as frg_interfaces

from nti.contentfragments.tests import ContentfragmentsLayerTest
from nti.contentfragments import html as frag_html

def _check_sanitized(inp, expect, expect_iface=frg_interfaces.IUnicodeContentFragment):
    was = frg_interfaces.IUnicodeContentFragment(inp)
    __traceback_info__ = inp, type(inp), was, type(was)
    assert_that(was, is_(expect.strip()))
    assert_that(was, verifiably_provides(expect_iface))
    return was

class TestHTTML(ContentfragmentsLayerTest):

    def test_sanitize_html(self):
        with open(os.path.join(os.path.dirname(__file__), 'contenttypes-notes-tosanitize.plist'), 'rb') as f:
            strings = load_plist(f)
        with open(os.path.join(os.path.dirname(__file__), 'contenttypes-notes-sanitized.txt')) as f:
            sanitized = f.readlines()

        for s in zip(strings, sanitized):
            _check_sanitized(s[0], s[1])

    def test_sanitize_data_uri(self):
        _ = _check_sanitized("<audio src='data:foobar' controls />",
                             u'<html><body><audio controls=""></audio></body></html>')

        _ = _check_sanitized("<audio data-id='ichigo' />",
                             u'<html><body><audio data-id="ichigo"></audio></body></html>')

    def test_normalize_html_text_to_par(self):
        html = u'<html><body><p style=" text-align: left;"><span style="font-family: \'Helvetica\';  font-size: 12pt; color: black;">The pad replies to my note.</span></p>The server edits it.</body></html>'
        exp = u'<html><body><p style="text-align: left;"><span>The pad replies to my note.</span></p><p style="text-align: left;">The server edits it.</p></body></html>'
        sanitized = _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)

        plain_text = frg_interfaces.IPlainTextContentFragment(sanitized)
        assert_that(plain_text, verifiably_provides(frg_interfaces.IPlainTextContentFragment))
        assert_that(plain_text, is_("The pad replies to my note.The server edits it."))

    def test_normalize_simple_style_color(self):
        html = u'<html><body><p><span style="color: black;">4</span></p></body></html>'
        exp = html
        sanitized = _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)
        assert_that(sanitized, is_(exp))

    def test_normalize_simple_style_font(self):
        html = u'<html><body><p><span style="font-family: sans-serif;">4</span></p></body></html>'
        exp = html
        sanitized = _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)

        assert_that(sanitized, is_(exp))

    def test_normalize_style_with_quoted_dash(self):
        html = u'<html><body><p style="text-align: left;"><span style="font-family: \'Helvetica-Bold\'; font-size: 12pt; font-weight: bold; color: black;">4</span></p></body></html>'
        exp = html
        sanitized = _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)
        assert_that(sanitized, is_(exp))

    def test_html_to_text(self):
        exp = frg_interfaces.HTMLContentFragment('<html><body><p style="text-align: left;"><span>The pad replies to my note.</span></p><p style="text-align: left;">The server edits it.</p></body></html>')
        plain_text = frg_interfaces.IPlainTextContentFragment(exp)
        assert_that(plain_text, verifiably_provides(frg_interfaces.IPlainTextContentFragment))
        assert_that(plain_text, is_("The pad replies to my note.The server edits it."))

    def test_rejected_tags(self):
        html = u'<html><body><div style=" text-align: left;">The text</div></body></html>'
        exp = 'The text'
        _check_sanitized(html, exp, frg_interfaces.IPlainTextContentFragment)

        html = u'<html><body><style>* { font: "Helvetica";}</style><p style=" text-align: left;">The text</div></body></html>'
        exp = u'<html><body><p style="text-align: left;">The text</p></body></html>'
        _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)

        html = u'<html><body><script><p>should be ignored</p> Other stuff.</script><p style=" text-align: left;">The text</div></body></html>'
        exp = u'<html><body><p style="text-align: left;">The text</p></body></html>'
        _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)

        html = u'foo<div><br></div><div>http://google.com</div><div><br></div><div>bar</div><div><br></div><div>http://yahoo.com</div>'''
        exp = u'<html><body>foo<br /><a href="http://google.com">http://google.com</a><br />bar<br /><a href="http://yahoo.com">http://yahoo.com</a></body></html>'
        _check_sanitized(html, exp, frg_interfaces.ISanitizedHTMLContentFragment)

    def test_pre_allowed(self):
        html = u'<html><body><pre>The text</pre></body></html>'
        exp = html
        _check_sanitized(html, exp)

    def test_blog_html_to_text(self):
        exp = u'<html><body>Independence<br />America<br />Expecting<br />Spaces</body></html>'
        plain_text = frg_interfaces.IPlainTextContentFragment(exp)
        assert_that(plain_text, verifiably_provides(frg_interfaces.IPlainTextContentFragment))
        assert_that(plain_text, is_("Independence\nAmerica\nExpecting\nSpaces"))

    def test_sanitize_user_html_chat(self):
        exp = u'<html><a href=\'http://tag:nextthought.com,2011-10:julie.zhu-OID-0x148a37:55736572735f315f54657374:hjJe3dfZMVb,"body":["5:::{\\"args\\\'>foo</html>'
        plain_text = frg_interfaces.IPlainTextContentFragment(exp)
        assert_that(plain_text, verifiably_provides(frg_interfaces.IPlainTextContentFragment))

        # idempotent
        assert_that(frag_html._sanitize_user_html_to_text(plain_text),
                    is_(same_instance(plain_text)))
        assert_that(frag_html._html_to_sanitized_text(plain_text),
                    is_(same_instance(plain_text)))

    def test_sanitize_img(self):
        html = '<html><body><img style="color: blue; text-align: left; max-width: 10px" href="foo"></body></html>'
        exp = '<html><body><img href="foo" style="color: blue; text-align: left; max-width: 100%;" /></body></html>'
        _check_sanitized(html, exp)

        html = '<html><body><img style="" href="foo"></body></html>'
        exp = '<html><body><img href="foo" style="max-width: 100%;" /></body></html>'
        _check_sanitized(html, exp)

        html = '<html><body><img max-width="1%" href="foo"></body></html>'
        exp = '<html><body><img href="foo" style="max-width: 100%;" /></body></html>'
        _check_sanitized(html, exp)

    def test_sanitize_empty_span(self):
        html = '<html><body><span></span></body></html>'
        exp = ''
        _check_sanitized(html, exp)

    def test_sanitize_remove_inner_elems(self):
        html = '<html><body><script><div /><span>Hi</span></script><style><span>hi</span></style></body></html>'
        exp = ''
        _check_sanitized(html, exp)

    def _allowed_attr_provider(self, attrs_to_allow):
        class TestAllowedAttrProvider(object):
            allowed_attributes = attrs_to_allow

        allowed_attribute_provider = TestAllowedAttrProvider()
        interface.alsoProvides(allowed_attribute_provider, (IAllowedAttributeProvider,))
        return allowed_attribute_provider

    def _test_allowed_attribute_provider(self, attr_name, included=True):
        html = '<html><body><a %s="my_value">Bobby Hagen</a></body></html>' % attr_name
        exp = html if included else '<html><body><a>Bobby Hagen</a></body></html>'
        _check_sanitized(html, exp)

    def test_allowed_attribute_provider(self):
        self._test_allowed_attribute_provider("abc", included=False)

        allowed_attrs = ["abc", "xyz"]
        allowed_attribute_provider = self._allowed_attr_provider(allowed_attrs)

        with _provide_utility(allowed_attribute_provider):
            for attr_name in allowed_attrs:
                self._test_allowed_attribute_provider(attr_name)

    def test_existing_links(self):
        allowed_attribute_provider = self._allowed_attr_provider(["data-nti-entity-href"])

        with _provide_utility(allowed_attribute_provider):
            # Ensure we properly handle html with existing anchors
            html = '<p><a data-nti-entity-href="http://www.google.com" ' \
                   'href="http://www.google.com">www.google.com</a></p>'
            exp = '<html><body><p><a data-nti-entity-href="http://www.google.com" ' \
                  'href="http://www.google.com">www.google.com</a></p></body></html>'
            _check_sanitized(html, exp)

    def test_link_creation(self):
        # Ensure links are created for url-like text following anchors
        html = '<p><a href="nextthought.com">NTI</a>www.google.com</p>'
        exp = '<html><body><p><a href="nextthought.com">NTI</a>' \
              '<a href="http://www.google.com">www.google.com</a></p></body></html>'
        _check_sanitized(html, exp)

    def test_nested_anchors(self):
        # Links should not be created for the url-like text and nesting
        # will be split
        html = '<p><a href="www.nextthought.com">www.nextthought.com' \
               '<a href="www.google.com">www.google.com</a></a></p>'
        exp = '<html><body><p><a href="www.nextthought.com">www.nextthought.com</a>' \
              '<a href="www.google.com">www.google.com</a></p></body></html>'
        _check_sanitized(html, exp)

    def test_disallowed(self):
        html = '<div>'
        _check_sanitized(html, u'')

    def test_disallowed_within_anchor(self):
        html = '<a href="www.nextthought.com"><div>test</div></a>'
        _check_sanitized(html, u'<html><body><a href="www.nextthought.com">test</a></body></html>')


@contextlib.contextmanager
def _provide_utility(util):
    gsm = component.getGlobalSiteManager()
    gsm.registerUtility(util, IAllowedAttributeProvider)
    try:
        yield
    finally:
        gsm.unregisterUtility(util, IAllowedAttributeProvider)
