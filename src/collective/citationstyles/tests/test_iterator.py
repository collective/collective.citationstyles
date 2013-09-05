import unittest2 as unittest
from bibliograph.core.interfaces import IBibliographicReference


from collective.citationstyles.testing import \
    COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING
from collective.citationstyles.iterator import BibliograpyIterator


class TestBibliograpyIterator(unittest.TestCase):

    layer = COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.bib_folder = self.portal.bib_folder

    def test_returns_contents_of_bibfolder_as_bibrefs(self):
        iterable = BibliograpyIterator(self.bib_folder)
        self.assertTrue(iterable is not None)
        listified = [item for item in iterable]
        self.assertEqual(len(self.bib_folder.objectValues()), len(listified))
        for item in iterable:
            self.assertTrue(IBibliographicReference.providedBy(item))

    def test_returns_single_bibitem_as_bibrefs(self):
        iterable = BibliograpyIterator(self.bib_folder.objectValues()[0])
        self.assertTrue(iterable is not None)
        listified = [item for item in iterable]
        self.assertEqual(1, len(listified))
        for item in iterable:
            self.assertTrue(IBibliographicReference.providedBy(item))

    def test_politely_skips_non_adaptable_content(self):
        class foo(object):
            pass

        iterable = BibliograpyIterator(foo())
        self.assertEqual(0, len([item for item in iterable]))
