"""Base importer"""
import typing
import unittest


class TestCase2(unittest.TestCase):
    def assertDictStructure(self,
                            structure: typing.Dict[typing.Hashable, typing.Type], d: dict):
        """
        Tests if a dict matches a defined structure

        :param structure: A dict of key: class pairs
        :type structure: Dict[Hashable, Class]
        :param d: dict to compare with
        :type d: dict
        """
        t = d.copy()
        [(self.assertIn(k, t), self.assertIsInstance(t.pop(k), v))
         for k, v in structure.items()]

        return t

    def assertDictStructureStrict(
            self,
            structure: typing.Dict[typing.Hashable, type], d: dict):
        """
        Tests if a dict matches strictly a defined structure

        :param structure: A dict of key: class pairs
        :type structure: Dict[Hashable, Class]
        :param d: dict to compare with
        :type d: dict
        """
        self.assertFalse(self.assertDictStructure(structure, d))
