#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

from nti.testing.matchers import implements, verifiably_provides

from zope import component

from ..interfaces import ITextLatexEscaper
from ..interfaces import ILatexContentFragment
from ..interfaces import PlainTextContentFragment
from ..interfaces import IPlainTextContentFragment

from ..latex import PlainTextToLatexFragmentConverter
from nti.contentfragments import latex as latex_mod

from . import ContentfragmentsLayerTest

def _tex_convert(val):
    if not IPlainTextContentFragment.providedBy(val):
        val = PlainTextContentFragment(val)
    return component.getAdapter(val, ILatexContentFragment)

def _tex_assert(val, answer):
    assert_that(_tex_convert(val), is_(answer))

class TestLatexTransforms(ContentfragmentsLayerTest):

    def _convert(self, val):
        return _tex_convert(val)

    def test_escaper(self):
        scaper = component.queryUtility(ITextLatexEscaper)
        assert_that(scaper, is_not(none()))
        assert_that(scaper(u'\u2026'), is_(r'\ldots '))

    def test_provides(self):
        assert_that(PlainTextToLatexFragmentConverter,
                    implements(ILatexContentFragment))
        assert_that(PlainTextToLatexFragmentConverter('foo'),
                    verifiably_provides(ILatexContentFragment))

    def test_trivial_escapes(self):
        assert_that(self._convert('$'), is_('\\$'))

    def test_equation_escape(self):
        assert_that(self._convert('13 + 6 = 19'), is_("$13 + 6 = 19$"))
        assert_that(self._convert(u'13 \u00d7 6 = 19'), is_(u"$13 \\times 6 = 19$"))
        assert_that(self._convert('13 + 6 = 19 Followed by text'), is_("$13 + 6 = 19$ Followed by text"))
        assert_that(self._convert('Preceded by text 13 + 6 = 19'), is_("Preceded by text $13 + 6 = 19$"))
        assert_that(self._convert('Ended with period: 13 + 6 = 19.'), is_("Ended with period: $13 + 6 = 19$."))
        assert_that(self._convert('An algebra eq 7x + 3y = 19z to solve.'),
                    is_('An algebra eq $7x + 3y = 19z$ to solve.'))

    def test_arith_sequence_eq_escape(self):
        assert_that(self._convert(u'Substituting 4 for a1 and 0.25 for d, we see that a35 = 4 + (34 \u00d7 0.25) = 4 + 8.5 = 12.5.'),
                    is_(u'Substituting 4 for a1 and 0.25 for d, we see that $a35 = 4 + (34 \\times 0.25) = 4 + 8.5 = 12.5$.'))

    def test_comment(self):
        _tex_assert(u'If 20% of the grapes', u'If 20\\% of the grapes')

    def test_trailing_question(self):
        _tex_assert(u'What is the positive difference between the value of 2 \u00d7 (3 + 4) and the value of 2 \u00d7 3 + 4?',
                    u'What is the positive difference between the value of $2 \\times (3 + 4)$ and the value of $2 \\times 3 + 4$?')
        _tex_assert(u'What is the value of 5 \u00d7 (11 + 4 \u00f7 4)?',
                    u'What is the value of $5 \\times (11 + 4 \\div 4)$?')

    def test_neq(self):
        _tex_assert(u'If something and x \u2260 y, then',
                    u'If something and $x \\neq y$, then')

    def test_punc_terminates_in_sequence(self):
        _tex_assert('is bounded by y = x, x = 5 and y = 1.',
                    'is bounded by $y = x$, $x = 5$ and $y = 1$.')

    def test_leading_or_trailing_space(self):
        _tex_assert(' abc ', ' abc ')

    def test_all_space(self):
        _tex_assert(' ', " ")

    def test_incomplete(self):
        _tex_assert('+', "+")

    def test_dangling(self):
        _tex_assert('1 +', "1 +")

    def test_equation_component(self):
        assert_that(latex_mod.is_equation_component(''), is_(''))
