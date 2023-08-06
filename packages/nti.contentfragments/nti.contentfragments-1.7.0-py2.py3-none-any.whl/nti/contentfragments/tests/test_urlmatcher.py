#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contentfragments import interfaces as frg_interfaces
from nti.contentfragments.urlmatcher import GrubberHyperlinkFormatter

from nti.contentfragments.tests import ContentfragmentsLayerTest

class TestUrlMatcher(ContentfragmentsLayerTest):

    formatter = GrubberHyperlinkFormatter()

    def test_simple(self):
        html = u'<html><head/><body>ichigo dies in http://www.bleachget.com/watch/bleach-episode-271</body></html>'
        exp = u'<html><head/><body>ichigo dies in <a href="http://www.bleachget.com/watch/bleach-episode-271">' + \
              u'http://www.bleachget.com/watch/bleach-episode-271</a></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))

    def test_simple_str(self):
        html = u'<html><head/><body>ichigo dies in http://www.bleachget.com/watch/bleach-episode-271</body></html>'
        exp = u'<html><head/><body>ichigo dies in <a href="http://www.bleachget.com/watch/bleach-episode-271">' + \
              u'http://www.bleachget.com/watch/bleach-episode-271</a></body></html>'
        assert_that(self.formatter.format(html), is_(exp))


    def test_double(self):
        html = u'<html><head/><body>yahoo in http://yahoo.com and google in http://www.google.com</body></html>'
        exp = u'<html><head/><body>yahoo in <a href="http://yahoo.com">http://yahoo.com</a> and google in ' + \
              u'<a href="http://www.google.com">http://www.google.com</a></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))

    def test_with_tail(self):
        html = u'<html><head/><body><p>does http://www.facebook.com sucks</p>yes check out http://www.nextthought.com</body></html>'
        exp = u'<html><head/><body><p>does <a href="http://www.facebook.com">http://www.facebook.com</a> sucks</p>' + \
              u'yes check out <a href="http://www.nextthought.com">http://www.nextthought.com</a></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))

    def test_others(self):
        html = u'<html><head/><body>my sec link https://www.chase.com</body></html>'
        exp = u'<html><head/><body>my sec link <a href="https://www.chase.com">https://www.chase.com</a></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))
        html = u'<html><head/><body>search with www.google.com to know everything</body></html>'
        exp = u'<html><head/><body>search with <a href="http://www.google.com">www.google.com</a> to know everything</body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))

    def test_nochange(self):
        html = u'<html><head/><body>are we there yet</body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(html))
        html = u'<html><head/><body>fly <a href="http://www.aa.com">aa</a> always</body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(html))
        html = u'<html><head/><body>fly <a href="http://www.aa.com">www.aa.com</a> always</body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(html))
        html = u'<html><head/><body>fly <a href="http://www.aa.com">www.aa.com</a> <a href="http://www.aa.com">www.aa.com</a></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(html))
        html = u'<html><head/><body><img src="http://www.aa.com/plane.jpg"/></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(html))

    def test_mailto(self):
        html = u'<html><head/><body>mailto:help@nextthought.com</body></html>'
        exp = u'<html><head/><body><a href="mailto:help@nextthought.com">help@nextthought.com</a></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))

    def test_utz(self):
        html = u"foo<div><br></div><div>http://google.com</div><div><br></div><div>bar</div><div><br></div><div>http://yahoo.com</div>"
        exp = u'<html><head/><body>foo<div><br/></div><div><a href="http://google.com">http://google.com</a></div>' +\
                '<div><br/></div><div>bar</div><div><br/></div><div><a href="http://yahoo.com">http://yahoo.com</a></div></body></html>'
        assert_that(self.formatter.format(frg_interfaces.IHTMLContentFragment(html)), is_(exp))
