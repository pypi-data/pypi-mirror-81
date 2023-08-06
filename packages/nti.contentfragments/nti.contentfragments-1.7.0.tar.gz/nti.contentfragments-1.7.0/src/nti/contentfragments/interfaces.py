#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Content-related interfaces.
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"
import sys
logger = __import__('logging').getLogger(__name__)
# pylint:disable=inherit-non-class,too-many-ancestors,no-self-argument,abstract-method
# pylint:disable=useless-object-inheritance
PY2 = str is bytes
PYPY = hasattr(sys, 'pypy_version_info')
PYPY2 = PY2 and PYPY
if PY2: # pragma: no cover
    import copy_reg # pylint:disable=import-error
    text_type = unicode # pylint:disable=undefined-variable
else:
    import copyreg as copy_reg
    text_type = str

from zope import component
from zope import interface

from zope.interface.common.collections import ISequence
from zope.interface.common.builtins import INativeString
from zope.interface.common.builtins import IByteString
from zope.interface.common.builtins import ITextString

from zope.contenttype import add_files as zc_add_files

from zope.mimetype import mtypes as mime_types

from zope.schema import NativeStringLine

from nti.schema.field import IndexedIterable

mime_types.setup()  # register interface classes and utilities if not already

resource_filename = __import__('pkg_resources').resource_filename


def _setup():
    types_data = resource_filename('nti.contentfragments', "types.csv")
    # Hmm. So this registers things in the zope.mimetype.types module
    # The ZCML directive registers them in the specified module (I think)
    # But we can't use that directive because we need them now in order to
    # implement them.
    data = mime_types.read(types_data)
    ifs = mime_types.getInterfaces(data)
    mime_types.registerUtilities(ifs, data)

    mime_map_file = resource_filename('nti.contentfragments', 'mime.types')
    zc_add_files([mime_map_file])
_setup()

# BWC aliases. These will be removed in the future.
IString = INativeString
IUnicode = ITextString
IBytes = IByteString


class IContentFragment(interface.Interface):
    """
    Base interface representing different formats that content can
    be in.
    """

class IUnicodeContentFragment(IContentFragment, ISequence):
    """
    Content represented as a unicode string.

    Although it is simplest to subclass :class:`unicode`, that is not required.
    At a minimum, what is required are the `__getitem__` method (and others
    declared by :class:`IReadSequence`), plus the `encode` method.

    .. versionchanged:: 1.3.0
       Extend ``zope.interface.common.collections.ISequence`` instead of the semi-deprecated
       ``zope.interface.common.sequence.IReadSequence``. Except on PyPy2, where
       ``ISequence`` cannot validate against unicode objects.
    """
    # TODO: extend IUnicode?

if PYPY2: # pragma: no cover
    IUnicodeContentFragment.__bases__ = tuple(
        x
        for x in IUnicodeContentFragment.__bases__
        if x is not ISequence
    )


@interface.implementer(IUnicodeContentFragment)
class UnicodeContentFragment(text_type):
    """
    Subclasses should override the :meth:`__add__` method
    to return objects that implement the appropriate (most derived, generally)
    interface.

    This object *DOES NOT* add a dictionary to the :class:`unicode` type.
    In particular, it should not be weak referenced. Subclasses that
    do not expect to be persisted in the ZODB *may* add additional attributes
    by adding to the ``__slots__`` field (not the instance value).
    """

    # We do need to allow the things used by zope.interface/zope.component
    _ZCA_KEYS = ('__provides__',)

    __slots__ = _ZCA_KEYS  # actually meaningless, but we simulate this with __getattr__ and __setattr__

    def __getattr__(self, name):
        raise AttributeError(name)

    def __setattr__(self, name, value):
        # We do allow the attributes used by the ZCA
        if name in type(self).__slots__:
            super(UnicodeContentFragment, self).__setattr__(name, value)
            return
        raise AttributeError(name, type(self))

    def __getattribute__(self, name):
        if name in ('__dict__', '__weakref__'):  # Though this does not actually prevent creating a weak ref
            raise AttributeError(name, type(self))
        if name == '__class__':
            return type(self)
        return text_type.__getattribute__(self, name)

    def __setstate__(self, state):
        # If we had any state saved due to bad pickles in the past
        # ignore it. Do support the ZCA attributes
        if state:
            for k in self.__slots__:
                v = state.pop(k, self)
                if v is not self:
                    text_type.__setattr__(self, k, v)
            # Anything left is bad and not supported. __parent__ was extremely common at one point
            if state and (len(state) > 1 or '__parent__' not in state):
                logger.warning("Ignoring bad state for %s: %s", self, state)

    def __getstate__(self):
        # Support just the ZCA attributes
        try:
            state = text_type.__getattribute__(self, '__dict__')
        except AttributeError:
            # Hmm, really is a slot
            try:
                state = {'__provides__': self.__provides__}
            except AttributeError:
                state = None
        if state:
            state = {k: v for k, v in state.items() if k in type(self).__slots__}
            return state

        return ()

    def __reduce_ex__(self, protocol):
        return (copy_reg.__newobj__,  # Constructor
                # Constructor args. Note we pass a real base unicode object;
                # otherwise, we get infinite recursion as pickle tries to
                # reduce use again using __unicode__
                (type(self), self.encode('utf-8').decode('utf-8')),
                self.__getstate__() or None,
                None,
                None)

    def __unicode__(self):
        """"
        We are-a unicode instance, but if we don't override this method,
        calling unicode(UnicodeContentFragment('')) produces a plain, base,
        unicode object, thus losing all our interfaces.
        """
        return self

    if not PY2:
        __str__ = __unicode__

        def __getslice__(self, i, j):
            # Part of IReadSequence, deprecated in 2.0, removed in 3,
            # but we still must implement it to comply with the iface.
            raise NotImplementedError()

    def __rmul__(self, times):
        result = text_type.__rmul__(self, times)
        if result is not self:
            result = self.__class__(result)
        return result

    def __mul__(self, times):
        result = text_type.__mul__(self, times)
        if result is not self:
            result = self.__class__(result)
        return result

    def translate(self, table):
        result = text_type.translate(self, table)
        if result is not self:
            result = self.__class__(result)
        return result

    def lower(self):
        result = text_type.lower(self)
        if result == self:
            return self  # NOTE this is slightly different than what a normal string does
        return self.__class__(result)

    def upper(self):
        result = text_type.upper(self)
        if result == self:
            return self  # NOTE this is slightly different than what a normal string does
        return self.__class__(result)

    # shut pylint up about 'bad container'; raise same error super does
    def __delitem__(self, i):
        raise TypeError()

    def __setitem__(self, k, v):
        raise TypeError()


IContentTypeTextLatex = getattr(mime_types, 'IContentTypeTextLatex')
class ILatexContentFragment(IUnicodeContentFragment, IContentTypeTextLatex):
    """
    Interface representing content in LaTeX format.
    """


@interface.implementer(ILatexContentFragment)
class LatexContentFragment(UnicodeContentFragment):
    pass


IContentTypeTextHtml = getattr(mime_types, 'IContentTypeTextHtml')
class IHTMLContentFragment(IUnicodeContentFragment, IContentTypeTextHtml):
    """
    Interface representing content in HTML format.
    """


IContentTypeTextRst = getattr(mime_types, 'IContentTypeTextRst')
class IRstContentFragment(IUnicodeContentFragment, IContentTypeTextRst):
    """
    Interface representing content in RST format.
    """


@interface.implementer(IRstContentFragment)
class RstContentFragment(UnicodeContentFragment):
    pass


# NOTE The implementations of the add methods go directly to
# unicode and not up the super() chain to avoid as many extra
# copies as possible

def _add_(self, other, tuples):
    result = text_type.__add__(self, other)
    for pair in tuples:
        if pair[0].providedBy(other):
            result = pair[1](result)
            break
    return result


class _AddMixin(object):
    _add_rules = ()

    def __add__(self, other):
        return _add_(self, other, self._add_rules)


@interface.implementer(IHTMLContentFragment)
class HTMLContentFragment(_AddMixin, UnicodeContentFragment):
    pass

HTMLContentFragment._add_rules = ((IHTMLContentFragment, HTMLContentFragment),)

class ISanitizedHTMLContentFragment(IHTMLContentFragment):
    """
    HTML content, typically of unknown or untrusted provenance,
    that has been sanitized for "safe" presentation in a generic,
    also unknown browsing context.
    Typically this will mean that certain unsafe constructs, such
    as <script> tags have been removed.
    """

@interface.implementer(ISanitizedHTMLContentFragment)
class SanitizedHTMLContentFragment(HTMLContentFragment):
    pass

# TODO: What about the rules for the other types?
SanitizedHTMLContentFragment._add_rules = \
    ((ISanitizedHTMLContentFragment, SanitizedHTMLContentFragment),) + \
    HTMLContentFragment._add_rules

IContentTypeTextPlain = getattr(mime_types, 'IContentTypeTextPlain')
class IPlainTextContentFragment(IUnicodeContentFragment, IContentTypeTextPlain):
    """
    Interface representing content in plain text format.
    """

@interface.implementer(IPlainTextContentFragment)
class PlainTextContentFragment(UnicodeContentFragment):
    pass

@interface.implementer(IPlainTextContentFragment)
@component.adapter(IPlainTextContentFragment)
def _plain_text_to_plain_text(text):
    # We shouldn't actually be able to get here.
    return text # pragma: no cover

from zope.schema.interfaces import ITokenizedTerm

class ICensoredTerm(ITokenizedTerm):
    """
    Base interface for a censored term
    """

class IProfanityTerm(ICensoredTerm):
    """
    Base interface for a profanity term
    """

class ICensoredUnicodeContentFragment(IUnicodeContentFragment):
    """
    A content fragment that has passed through a censoring process to
    attempt to ensure it is safe for display to its intended audience (e.g.,
    profanity has been removed if the expected audience is underage/sensitive to
    that).

    The rules for censoring content will be very context specific. In
    particular, it will depend on *who* you are, and *where* you are
    adding/editing content. The *who* is important to differentiate
    between, e.g., students and teachers. The *where* is important to
    differentiate between, say, a public forum, and your private notes, or
    between your Human Sexuality textbook and your Calculus textbook.

    For this reason, the censoring process will typically utilize
    multi-adapters registered on (creator, content_unit). Contrast this with
    sanitizing HTML, which always follows the same process.
    """

@interface.implementer(ICensoredUnicodeContentFragment)
class CensoredUnicodeContentFragment(_AddMixin, UnicodeContentFragment):
    pass

CensoredUnicodeContentFragment._add_rules = (
    (ICensoredUnicodeContentFragment, CensoredUnicodeContentFragment),
    (IUnicodeContentFragment, UnicodeContentFragment)
)

class ICensoredPlainTextContentFragment(IPlainTextContentFragment, ICensoredUnicodeContentFragment):
    pass

@interface.implementer(ICensoredPlainTextContentFragment)
class CensoredPlainTextContentFragment(PlainTextContentFragment):
    pass

PlainTextContentFragment.censored = lambda s, n: CensoredPlainTextContentFragment(n)
CensoredPlainTextContentFragment.censored = lambda s, n: CensoredPlainTextContentFragment(n)

class ICensoredHTMLContentFragment(IHTMLContentFragment, ICensoredUnicodeContentFragment):
    pass

@interface.implementer(ICensoredHTMLContentFragment)
class CensoredHTMLContentFragment(HTMLContentFragment):
    pass

CensoredHTMLContentFragment._add_rules = \
    ((ICensoredHTMLContentFragment, CensoredHTMLContentFragment),) + \
    CensoredUnicodeContentFragment._add_rules
CensoredHTMLContentFragment.censored = lambda s, n: CensoredHTMLContentFragment(n)

class ICensoredSanitizedHTMLContentFragment(ISanitizedHTMLContentFragment, ICensoredHTMLContentFragment):
    pass

@interface.implementer(ICensoredSanitizedHTMLContentFragment)
class CensoredSanitizedHTMLContentFragment(CensoredHTMLContentFragment):
    pass

# The rules here place sanitization ahead of censoring, because sanitization
# can cause security problems for end users; censoring is just offensive
CensoredSanitizedHTMLContentFragment._add_rules = (
    ((ICensoredSanitizedHTMLContentFragment, CensoredSanitizedHTMLContentFragment),
     (ISanitizedHTMLContentFragment, SanitizedHTMLContentFragment),)
    + CensoredHTMLContentFragment._add_rules
    + HTMLContentFragment._add_rules
)

HTMLContentFragment.censored = lambda s, n: CensoredHTMLContentFragment(n)
UnicodeContentFragment.censored = lambda s, n: CensoredUnicodeContentFragment(n)
SanitizedHTMLContentFragment.censored = lambda s, n: CensoredSanitizedHTMLContentFragment(n)
CensoredSanitizedHTMLContentFragment.censored = lambda s, n: CensoredSanitizedHTMLContentFragment(n)

# See http://code.google.com/p/py-contentfilter/
# and https://hkn.eecs.berkeley.edu/~dyoo/python/ahocorasick/

class ICensoredContentScanner(interface.Interface):
    """
    Something that can perform censoring.

    Variations of censoring scanners will be registered
    as named utilities. Particular censoring solutions (the adapters discussed
    in :class:`ICensoredUnicodeContentFragment`) will put together
    a combination of these utilities to produce the desired result.

    The censoring process can further be broken down into two parts:
    detection of unwanted content, and reacting to unwanted content. For example,
    reacting might consist of replacing the content with asterisks in plain text,
    or a special span in HTML, or it might throw an exception to disallow the content
    altogether. This object performs the first part.

    The names may be something like MPAA ratings, or they may follow other categories.
    """

    def scan(content_fragment):
        """
        Scan the given content fragment for censored terms and return
        their positions as a sequence (iterator) of two-tuples (start,
        end). The returned tuples should be non-overlapping.
        """

class ICensoredContentStrategy(interface.Interface):
    """
    The other half of the content censoring process explained in
    :class:`ICensoredContentScanner`, responsible for taking action
    on censoring content.
    """

    def censor_ranges(content_fragment, censored_ranges):
        """
        Censors the content fragment appropriately and returns the censored value.

        :param content_fragment: The fragment being censored.
        :param censored_ranges: The ranges of illicit content as produced by
            :meth:`ICensoredContentScanner.scan`; they are not guaranteed to be in any
            particular order so you may need to sort them with :func:`sorted` (in reverse)
        :return: The censored content fragment, if any censoring was done to it.
            May also raise a :class:`ValueError` if censoring is not
            allowed and the content should be thrown away.
        """

class ICensoredContentPolicy(interface.Interface):
    """
    A top-level policy puts together detection of content ranges
    to censor with a strategy to censor them
    """

    def censor(content_fragment, context):
        """
        Censors the content fragment appropriately and returns the censored value.

        :param content_fragment: The fragment being censored.
        :param context: The object that this content fragment should be censored
            with regard to. For example, the fragment's container or composite
            object that will hold the fragment.
        :return: The censored content fragment, if any censoring was done to it.
            May also raise a :class:`ValueError` if censoring is not
            allowed and the content should be thrown away.
        """

class IHyperlinkFormatter(interface.Interface):

    def find_links(text):
        """
        Given a string of `text`, look through it for hyperlinks and find them.

        :return: A sequence of strings and `lxml.etree.Element` objects representing
            the plain text and detected links, in order, within the given text.
        """

    def format(html_fragment):
        """
        Process the specified ``IHTMLContentFragment`` and scan through and convert any
        plain text links recognized by the this object and inserting new ``<a>`` elements,
        """

class ICensoredContentEvent(interface.Interface):
    content_fragment = interface.Attribute("The content that was censored")
    censored_content = interface.Attribute("The censored content")
    name = interface.Attribute("The name of the attribute under which the censor content will be assigned.")
    context = interface.Attribute("The context object where the object will be assigned to.")

@interface.implementer(ICensoredContentEvent)
class CensoredContentEvent(object):

    def __init__(self, content_fragment, censored_content, name=None, context=None):
        self.content_fragment = content_fragment
        self.censored_content = censored_content
        self.name = name
        self.context = context

class ITextLatexEscaper(interface.Interface):

    def __call_(text):
        """
        scape the specifed text
        """

# Punctuation

class IPunctuationMarkExpression(interface.Interface):
    """
    marker interface for punctuation regular expression
    """
IPunctuationCharExpression = IPunctuationMarkExpression

class IPunctuationMarkExpressionPlus(interface.Interface):
    """
    marker interface for punctuation + space regular expression
    """
IPunctuationCharExpressionPlus = IPunctuationMarkExpressionPlus

class IPunctuationMarkPattern(interface.Interface):
    """
    marker interface for punctuation regular expression pattern
    """
IPunctuationCharPattern = IPunctuationMarkPattern

class IPunctuationMarkPatternPlus(interface.Interface):
    """
    marker interface for punctuation + space regular expression pattern
    """
IPunctuationCharPatternPlus = IPunctuationMarkPatternPlus

## Schema Fields

from zope.schema.interfaces import IObject
from zope.schema.interfaces import IText
from zope.schema.interfaces import ITextLine

class ITextUnicodeContentFragmentField(IObject, IText):
    """
    A :class:`zope.schema.Text` type that also requires the object implement
    an interface descending from :class:`~.IUnicodeContentFragment`.

    .. versionadded:: 1.2.0
    """

class ITextLineUnicodeContentFragmentField(IObject, ITextLine):
    """
    A :class:`zope.schema.TextLine` type that also requires the object implement
    an interface descending from :class:`~.IUnicodeContentFragment`.

    .. versionadded:: 1.2.0
    """

class ILatexFragmentTextLineField(ITextLineUnicodeContentFragmentField):
    """
    A :class:`~zope.schema.TextLine` that requires content to be in LaTeX format.

    .. versionadded:: 1.2.0
    """


class IPlainTextLineField(ITextLineUnicodeContentFragmentField):
    """
    A :class:`~zope.schema.TextLine` that requires content to be plain text.
    """


class IHTMLContentFragmentField(ITextUnicodeContentFragmentField):
    """
    A :class:`~zope.schema.Text` type that also requires the object implement
    an interface descending from :class:`.IHTMLContentFragment`.

    .. versionadded:: 1.2.0
    """


class ISanitizedHTMLContentFragmentField(IHTMLContentFragmentField):
    """
    A :class:`Text` type that also requires the object implement
    an interface descending from :class:`.ISanitizedHTMLContentFragment`.

    .. versionadded:: 1.2.0
    """

class IPlainTextField(ITextUnicodeContentFragmentField):
    """
    A :class:`zope.schema.Text` that requires content to be plain text.

    .. versionadded:: 1.2.0
    """


class IRstContentFragmentField(ITextUnicodeContentFragmentField):
    """
    A :class:`~zope.schema.Text` type that also requires the object implement
    an interface descending from :class:`.IRstContentFragment`.

    .. versionadded:: 1.6.0
    """


class ITagField(IPlainTextLineField):
    """
    Requires its content to be only one plain text word that is lowercased.

    .. versionadded:: 1.2.0
    """

class IAllowedAttributeProvider(interface.Interface):
    """
    A way to provide a whitelist of additional attribute names that would be
    allowed while parsing a content fragment, thus extending the attributes
    already allowed.

    .. versionadded:: 1.4.0
    """

    allowed_attributes = IndexedIterable(title=u"An iterable of attribute names allowed in a particular context",
                                         value_type=NativeStringLine(title=u"The attribute name"),
                                         default=(),
                                         required=False)
