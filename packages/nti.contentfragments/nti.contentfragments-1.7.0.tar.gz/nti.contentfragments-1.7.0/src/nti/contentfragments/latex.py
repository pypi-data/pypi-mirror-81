#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementations of content fragment transformers for latex.

.. $Id: latex.py 85352 2016-03-26 19:08:54Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

from zope import component
from zope import interface

from nti.contentfragments.interfaces import ITextLatexEscaper
from nti.contentfragments.interfaces import LatexContentFragment
from nti.contentfragments.interfaces import ILatexContentFragment
from nti.contentfragments.interfaces import IPlainTextContentFragment

# Map from unicode to tex name
_TEX_OPERATORS = [(u'\u00d7', u'\\times'),
                  (u'\u2013', u'-'),
                  (u'\u2212', u'-'),
                  (u'\u2260', u'\\neq'),
                  (u'\u00f7', u'\\div'),
                  (u'\u2026', u'\\ldots '),
                  (u'\u221a', u'\\surd'),  # radicand
                  (u'\u2192', u'\\rightarrow'),
                  (u'\uf0d0', u'\\angle'),
                  (u'\uf044', u'\\triangle'),
                  (u'\u2248', u'\\approx')]
_TEX_OPERATOR_MAP = {ord(_k): _v for _k, _v in _TEX_OPERATORS}

# charmap_extn = {
#   u'\u20ac'.encode('utf8'): r'\euro ',
#   u'\u00bd'.encode('utf8'): r'$\frac{1}{2}$',
#   u'\uf020'.encode('utf8'): " ", # 0xef80a0
#   u'\uf02c'.encode('utf8'): " ", # 0xef80ac
#   u'\uf02f'.encode('utf8'): "/", # 0xef80af
#   u'\uf02e'.encode('utf8'): ".",
#   u'\uf06c'.encode('utf8'): " ", # 0xef80ac
#   u'\u2022'.encode('utf8'): r"*", # 0xe280a2 (bullet)
#   u'\u2212'.encode('utf8'): r"-", # 0xe28892
#   u'\u2264'.encode('utf8'): r"$\le$", # 0xef89a4
#   u'\u2265'.encode('utf8'): r"$\ge$", # 0xef89a5
#   u'\u2248'.encode('utf8'): r"$\approx$", # 0xef8988
#   u'\u221E'.encode('utf8'): r"$\infty$", # 0xef889e
#   u'\u03bc'.encode('utf8'): r'$\mu$', # 0xcebc
#   u'\u03A3'.encode('utf8'): r'$\Sigma$', # 0xcEA3
#   u'\uf032'.encode('utf8'): r'$\prime$', # 0xef80b2
#   u'\u03b1'.encode('utf8'): r'$\alpha$', # 0xceb1
#   u'\u03b2'.encode('utf8'): r'$\beta$', # 0xceb2
#   u'\u03b3'.encode('utf8'): r'$\gamma$', # 0xceb3
#   u'\u03c1'.encode('utf8'): r'$\rho$', # 0xcf81
#   u'\u03c3'.encode('utf8'): r'$\sigma$', # 0xcf83
#   u'\u00ad'.encode('utf8'): r'', # 0xc2ad (soft hyphen)
#   u'\u03A0'.encode('utf8'): r'$\Pi$', # 0xc2A0
#   u'\u0394'.encode('utf8'): r'$\Deltae$', # 0xce94
#   u'\u00b5'.encode('utf8'): r'$\mu$', # 0xc2ad (soft hyphen)
#   # This is actually the CENT SIGN, but in the symbol font
#   # it comes in as prime.
#   u'\u00a2'.encode('utf8'): r'$\prime$', # 0xc2c2

_escapes = [(u'$', u'\\$'),
            (u'%', u'\\%'),
            (u'\xa2', u'$\\prime$'),  # \uf0
            (u'\xad', u''),
            (u'\xb5', u'$\\mu$'),
            (u'\xbd', u'$\\frac{1}{2}$'),
            (u'\xd7', u'$\\times$'),
            (u'\xf7', u'$\\div$'),
            (u'\u0394', u'$\\Delta$'),
            (u'\u03a0', u'$\\Pi$'),
            (u'\u03a3', u'$\\Sigma$'),
            (u'\u03b1', u'$\\alpha$'),
            (u'\u03b2', u'$\\beta$'),
            (u'\u03b3', u'$\\gamma$'),
            (u'\u03bc', u'$\\mu$'),
            (u'\u03c0', u'$\\pi$'),
            (u'\u03c1', u'$\\rho$'),
            (u'\u03c3', u'$\\sigma$'),
            (u'\u2013', u'-'),
            (u'\u2014', u'---'),
            (u'\u2019', u"'"),
            (u'\u201c', u'``'),
            (u'\u201d', u"''"),
            (u'\u2022', u'*'),
            # JAM: Why is this commented out? It has been since the
            # first revision of this file, but it seems valid
            # (u'\u2026', u'$\\ldots$'),
            (u'\u20ac', u'\\euro '),
            (u'\u2192', u'$\\rightarrow$'),
            (u'\u2212', u'-'),
            (u'\u2212', u'-'),
            (u'\u221a', u'$\\surd$'),
            (u'\u221e', u'$\\infty$'),
            (u'\u2248', u'$\\approx$'),
            (u'\u2248', u'$\\approx$'),
            (u'\u2260', u'$\\neq$'),
            (u'\u2264', u'$\\le$'),
            (u'\u2265', u'$\\ge$'),
            (u'\uf020', u' '),
            (u'\uf02c', u' '),
            (u'\uf02e', u'.'),
            (u'\uf02f', u'/'),
            (u'\uf032', u'$\\prime$'),
            (u'\uf044', u'$\\triangle$'),
            (u'\uf06c', u' '),
            (u'\uf0d0', u'$\\angle$'),
            (u'. . .', u'\\ldots '),
            (u'\u2026', u'\\ldots '),
            (u'\u00A7', u'\\S')]

def _escape_tex(text):
    escaped_text = text
    for escape in _escapes:
        escaped_text = escaped_text.replace(escape[0], escape[1])
    return escaped_text

@interface.implementer(ITextLatexEscaper)
class _DefaultTextLatexEscaper(object):

    __slots__ = ()

    def __call__(self, text):
        return _escape_tex(text)

def escape_tex(text, name=u''):
    scaper = component.queryUtility(ITextLatexEscaper, name=name)
    scaper = _escape_tex if scaper is None else scaper
    return scaper(text)

_PLAIN_BINARY_OPS = (u'+', u'-', u'*', u'/', u'=', u'<', u'>', u'\u2260')
_UNICODE_OPS = [_x[0] for _x in _TEX_OPERATORS]

_PLAIN_ACCEPTS = (u'(', u')')

_naturalNumberPattern = re.compile(u'^[0-9]+[.?,]?$')  # Optional trailing punctuation
_realNumberPattern = re.compile(u'^[0-9]*\\.[0-9]*[.?,]?$')  # Optional trailing punctuation
_SIMPLE_ALGEBRA_TERM_PAT = re.compile(r"^[0-9]+\.?[0-9]*[b-zB-Z" + '\u03C0]$')
_PRE_SIMPLE_ALGEBRA_TERM_PAT = re.compile(r"^[a-zA-Z][0-9]+\.?[0-9]*$")
_SIMPLE_ALGEBRA_VAR = re.compile(u'^[a-zA-Z]$')

_TRAILING_PUNCT = (u',', u'.', u'?')

def is_equation_component(token):
    if not token:
        return token  # False for empty tokens
    return (token in _PLAIN_BINARY_OPS
            # Match '('
            or token in _PLAIN_ACCEPTS
            # Match '(7'
            or (token.startswith(u'(') and is_equation_component(token[1:]))
            # Match '7)'
            or (token.endswith(u')') and is_equation_component(token[0:-1]))
            or (token[-1] in _TRAILING_PUNCT and is_equation_component(token[0:-1]))
            or token in _UNICODE_OPS
            or _naturalNumberPattern.match(token)
            or _realNumberPattern.match(token)
            or _SIMPLE_ALGEBRA_TERM_PAT.match(token)
            or _PRE_SIMPLE_ALGEBRA_TERM_PAT.match(token)
            or _SIMPLE_ALGEBRA_VAR.match(token))

def cleanup_equation_tokens(tokens):
    """
    Perform cleanups on the individual tokens that make up an
    equation before converting it to string form.

    :return: A 3-tuple: (before string, tokens, after_string)
    """
    # This is a partial implementation that grows as needed
    if tokens[-1][-1] in _TRAILING_PUNCT:
        punct = tokens[-1][-1]
        tokens = list(tokens)
        tokens[-1] = tokens[-1][0:-1]
        return (u'', tokens, punct)
    return (u'', tokens, u'')

@interface.implementer(ILatexContentFragment)
@component.adapter(IPlainTextContentFragment)
def PlainTextToLatexFragmentConverter(plain_text, text_scaper=u''):
    """
    Attempt to convert plain-text strings into LaTeX strings
    by detecting equations/expressions that could be rendered in
    latex markup.
    """
    # We do a crappy job of trying to parse out expression-like things
    # with a hand-rolled parser. There are certainly better ways. One might
    # be to extract the math parsing algorithm from plasTeX; we'd still have to
    # figure out what makes sense, though

    # SAJ: Before we do anything test and see if we were give a run of pure white
    # space.  If so, just return what we were given.

    if plain_text.isspace():
        return LatexContentFragment(plain_text)

    # First, replace some whitespace sensitive tokens
    plain_text = plain_text.replace(u'. . .', u'\u2026')  # Ellipsis

    # Then, tokenize on whitespace. If the math is poorly delimited, this
    # will fail
    tokens = plain_text.split()

    # Run through until we find an operator. Back up while the previous
    # tokens are numbers. Go forward while the tokens are numbers or operators.
    # repeat until we have consumed all the tokens
    accum = []

    # Each time through the loop we'll either consume an equation and everything
    # before it, or we'll take no action. When we reach the end naturally,
    # everything left is not an equation
    i = 0
    while i < len(tokens):
        if tokens[i] in _PLAIN_BINARY_OPS:
            pointer = i - 1
            while pointer >= 0:
                if is_equation_component(tokens[pointer]):
                    pointer -= 1
                else:
                    break
            if pointer == i - 1:
                # We didn't move backwards at all. This is not part of an equation
                i += 1
                continue
            beginning = pointer + 1  # We moved the cursor before the beginning
            pointer = i + 1
            while pointer < len(tokens):
                token = tokens[pointer]
                if is_equation_component(token):
                    pointer += 1
                    if token[-1] in _TRAILING_PUNCT:
                        break
                else:
                    break
            if pointer == i + 1:
                # We didn't move forwards at all. Hmm. A dangling
                # part of an equation.
                i += 1
                continue
            end = pointer
            eq_tokens = tokens[beginning:end]
            bef, eq_tokens, aft = cleanup_equation_tokens(eq_tokens)
            eq = u' '.join(eq_tokens)
            eq = eq.translate(_TEX_OPERATOR_MAP)
            eq = bef + u'$' + eq + u'$' + aft

            # Everything before us goes in the accumulator
            accum.extend([escape_tex(x, name=text_scaper) for x in tokens[0:beginning]])
            # and then us
            accum.append(eq)
            # and now we can remove the beginning and start over
            del tokens[0:end]
            i = 0
        else:
            # Not a constituent, go forward
            i += 1

    # Any tokens left go in the accumulator
    accum.extend([escape_tex(x, name=text_scaper) for x in tokens])

    # SAJ: If the fragment starts or ends with a space, respect that
    if plain_text and plain_text[0].isspace():
        accum.insert(0, u'')

    if plain_text and plain_text[-1].isspace():
        accum.append(u'')

    result = LatexContentFragment(u' '.join(accum))
    return result
