import unittest
from thearbiter.validator import Arbiter, TooManyArgumentsError


class ArbiterTestCase(unittest.TestCase):
    def test_validator_with_list(self):
        """
        Tests a simple list validation with all arguments provided.
        """
        arbiter = Arbiter(['a', 'b'])
        self.assertTrue(arbiter.validate_args(a=1, b=2))

    def test_validator_missing_attribute_with_list(self):
        """
        Ensures a simple list throws an exception when an arguments is missing.
        """
        arbiter = Arbiter(['a', 'b'])
        with self.assertRaises(AttributeError):
            arbiter.validate_args(b=2)

    def test_validator_with_simple_or(self):
        """
        A simple "OR" logic test.
        """
        arbiter = Arbiter({'or': ['a', 'b', 'c']})
        self.assertTrue(arbiter.validate_args(a=1))
        self.assertTrue(arbiter.validate_args(b=1))
        self.assertTrue(arbiter.validate_args(c=1))
        self.assertTrue(arbiter.validate_args(a=1, b=2))
        self.assertTrue(arbiter.validate_args(b=1, c=2))
        self.assertTrue(arbiter.validate_args(a=1, b=2, c=3))

    def test_validator_with_simple_xor(self):
        """
        Testing "XOR" logic with valid attributes.
        """
        arbiter = Arbiter({'xor': ['a', 'b', 'c']})
        self.assertTrue(arbiter.validate_args(a=1))
        self.assertTrue(arbiter.validate_args(b=1))
        self.assertTrue(arbiter.validate_args(c=1))

    def test_validator_too_many_args(self):
        """
        Testing "XOR" logic to make sure exclusivity is honored.
        """
        arbiter = Arbiter({'xor': ['a', 'b', 'c']})
        with self.assertRaises(TooManyArgumentsError):
            arbiter.validate_args(a=1, b=2)

    def test_validator_nested_xor(self):
        """
        Test "XOR" with a nested list of requirements that need to be met.
        """
        arbiter = Arbiter({'xor': ['a', ['b', 'c']]})  # Must have 'a', or 'b' and 'c' together.
        self.assertTrue(arbiter.validate_args(a=1))
        self.assertTrue(arbiter.validate_args(b=1,c=2))

    def test_nested_mix_of_requirements(self):
        """
        A complex test of nexted requirements.
        """
        arbiter = Arbiter([
            'a',                       # Must have a
            {'or_b_c': ['b', 'c']},    # and either b or c (or both)
            {'xor_e_f': ['e', 'f']},   # and either e or f (but not both)
            {'or': [                   # and (g or h exclusively) or (i or j or both)
                {'xor': ['g', 'h']},
                {'or': ['i', 'j']}
            ]}
        ])

        self.assertTrue(arbiter.validate_args(a=1, b=2, e=3, g=4))
        self.assertTrue(arbiter.validate_args(a=1, c=2, f=3, h=4))
        self.assertTrue(arbiter.validate_args(a=1, b=1.3, c=2, f=3, i=4))
        self.assertTrue(arbiter.validate_args(a=1, b=2, c=3, f=4, g=5, i=6, j=7))

    def test_nested_mix_bad_args(self):
        """
        A complex test of nexted requirements.
        """
        arbiter = Arbiter([
            'a',                       # Must have a
            {'or_b_c': ['b', 'c']},    # and either b or c (or both)
            {'xor_e_f': ['e', 'f']},   # and either e or f (but not both)
            {'or': [                   # and (g or h exclusively) or (i or j or both)
                {'xor': ['g', 'h']},
                {'or': ['i', 'j']}
            ]}
        ])

        with self.assertRaises(TooManyArgumentsError):
            arbiter.validate_args(a=1, b=1.3, c=2, e=3, f=3, i=4)

        with self.assertRaises(TooManyArgumentsError):
            arbiter.validate_args(a=1, b=2, c=3, f=4, g=5, h=5, i=6, j=7)

        with self.assertRaises(AttributeError):
            arbiter.validate_args(a=1, b=2, c=3, f=4)

    def test_invalid_attribute_type(self):
        """
        Tests exceptions thrown for invalid types in required attributes
        """

        bad_list_arbiter = Arbiter([1])  # 1 is not valid.
        with self.assertRaises(TypeError):
            bad_list_arbiter.validate_args(a=1)

        bad_list_arbiter.required_args = [Exception("this shouldn't work")]
        with self.assertRaises(TypeError):
            bad_list_arbiter.validate_args(a=1)

    def test_dict_operation_invalid(self):
        arbiter = Arbiter({'Not going to work': ['a', 'b']})  # Key Not "or" or "xor"
        with self.assertRaises(KeyError):
            arbiter.validate_args(a=1)

    def test_dict_value_not_list(self):
        """
        Ensures the dict path throws a TypeError when the value is not a list.
        """

        arbiter = Arbiter({'or': 'a'})
        with self.assertRaises(TypeError):
            arbiter.validate_args(a=1)


if __name__ == '__main__':
    unittest.main()
