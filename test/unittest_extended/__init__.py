"""Base importer"""
import typing
from unittest import *


class TestCase2(TestCase):
    def assertDictStructure(self,
                            structure: typing.Dict[typing.Hashable, typing.ClassVar], d: dict):
        """
        Tests if a dict matches a defined structure

        :param structure: A dict of key: class pairs
        :type structure: Dict[Hashable, Class]
        :param d: dict to compare with
        :type d: dict
        """
        [(self.assertIn(k, d), self.assertIsInstance(v, d.pop(k)))
         for k, v in structure.items()]

        return d

    def assertDictStructureStrict(
            self,
            structure: typing.Dict[typing.Hashable, typing.ClassVar], d: dict):
        """
        Tests if a dict matches strictly a defined structure

        :param structure: A dict of key: class pairs
        :type structure: Dict[Hashable, Class]
        :param d: dict to compare with
        :type d: dict
        """
        self.assertFalse(self.assertDictStructure(structure, d))
