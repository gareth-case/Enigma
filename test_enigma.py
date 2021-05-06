"""
Unit tests for the enigma_machine module.

Example:
    $ python test_enigma.py
"""

import unittest

from enigma_machine import EnigmaMachine


class RotorTestCase(unittest.TestCase):
    """
    Test case for an Enigma Rotor.
    Methods tested:
        __init__
        turn_rotor
        apply_ring_setting
        map_letter
    """
    def setUp(self):
        """
        Construct an Enigma Rotor and a few cases of invalid parameters.
        """
        self.rotor = EnigmaMachine.Rotor(rotor_type='I',
                                         position='A',
                                         ring_setting='A')
        self.invalid_rotor_types = ['VII', 1, '1']
        self.invalid_rotor_positions = [1, '1', 'AB']

    def test_init(self):
        """
        Tests the constructor for an Enigma Rotor.
        Checks that rotors cannot be constructed with invalid parameters.
        """
        # Check invalid mappings
        for rotor_type in self.invalid_rotor_types:
            with self.assertRaises(ValueError) as context:
                EnigmaMachine.Rotor(rotor_type=rotor_type)
            self.assertTrue(context.exception)

        # Check invalid position
        for position in self.invalid_rotor_positions:
            with self.assertRaises(ValueError) as context:
                EnigmaMachine.Rotor(position=position)
            self.assertTrue(context.exception)

    def test_turn_rotor(self):
        """
        Tests the turn_rotor method for an Enigma Rotor.
        Checks that turning rotor advances position but changes nothing else.
        """
        prev_mapping = self.rotor.mapping
        prev_notch = self.rotor.notch
        prev_ring_setting = self.rotor.ring_setting
        self.rotor.turn_rotor()
        self.assertEqual(self.rotor.position, 'B', 'Rotor turned incorrectly')
        self.assertEqual(prev_mapping, self.rotor.mapping, 'Mapping altered')
        self.assertEqual(prev_notch, self.rotor.notch, 'Notch altered')
        self.assertEqual(prev_ring_setting, self.rotor.ring_setting,
                         'Ring setting altered')

    def test_apply_ring_setting(self):
        """
        Tests the apply_ring_setting method for an Enigma Rotor.
        Checks that position of the ring setting performs the correct Caeser
        and positional shift to the rotor mapping.
        """
        self.rotor.apply_ring_setting('D')
        expected_rotor_mapping = 'UFMHNPIOJGTYCQWRZBKAXVSDLE'
        self.assertEqual(self.rotor.mapping, expected_rotor_mapping)

    def test_map_letter(self):
        """
        Tests the map_letter method for an Enigma Rotor.
        Performs a test case of mapping a letter through the rotor.
        With these settings, A should map to E.
        """
        rotor = EnigmaMachine.Rotor(rotor_type='I',
                                    position='B',
                                    ring_setting='D')

        input_letter = 'A'
        expected_letter = 'E'
        actual_letter = rotor.map_letter(input_letter)
        self.assertEqual(actual_letter, expected_letter)

        # Test reverse. Should put the original letter.
        expected_reverse = rotor.map_letter(expected_letter, reverse=True)
        self.assertEqual(input_letter, expected_reverse)


class ReflectorTestCase(unittest.TestCase):
    """
    Test case for an Enigma Reflector.
    Methods tested:
        __init__
        map_letter
    """
    def setUp(self):
        """
        Construct an Enigma Reflector and a few cases of invalid parameters.
        """
        self.reflector = EnigmaMachine.Reflector(reflector_mapping='A')
        self.custom_reflector = EnigmaMachine.Reflector(
            reflector_mapping='BADCFEHGJILKNMPORQTSVUXWZY')
        self.invalid_reflector_mappings = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ',  # 'C'
                                           'D',  # No 'D' reflector
                                           'ABCDEFGHIJKLMNOPQRSTUVWXY']  # 25ch

    def test_init(self):
        """
        Tests the constructor for an Enigma Reflector.
        Checks that reflectors cannot be constructed with invalid parameters
        such as mappings that don't pair letters together, have invalid length
        or aren't a standard Reflector letter (A B or C).
        """
        for mapping in self.invalid_reflector_mappings:
            with self.assertRaises(ValueError) as context:
                EnigmaMachine.Reflector(reflector_mapping=mapping)
            self.assertTrue(context.exception)

    def test_map_letter(self):
        """
        Tests the map_letter method for an Enigma Reflector.
        Performs a few test cases of mapping a letter through the
        reflector.
        """
        letter_inputs = ['A', 'B', 'G', 'Z']
        expected_outputs = ['B', 'A', 'H', 'Y']
        for i in range(len(letter_inputs)):
            actual_output = self.reflector.map_letter(letter_inputs[i])
            self.assertTrue(actual_output, expected_outputs[i])


class PlugboardTestCase(unittest.TestCase):
    """
    Test case for an Enigma Plugboard.
    Methods tested:
        __init__
        map_letter
    """
    def setUp(self):
        """
        Construct an Enigma Plugboard and a few cases of invalid parameters.
        """
        self.plugboard = EnigmaMachine.Plugboard(
            steckered_pairing='AM FI NV PS TU WZ')
        self.invalid_steckered_pairing = ['AB AC',
                                          'ABC',
                                          'AB DC EF HG I',
                                          'AM DF GI  XY']

    def test_init(self):
        """
        Tests the constructor for an Enigma Plugboard.
        Checks that plugboards cannot be constructed with invalid parameters
        such as mappings that don't pair letters together or have invalid
        length.
        """
        with self.assertRaises(ValueError) as context:
            EnigmaMachine.Plugboard(
                steckered_pairing=self.invalid_steckered_pairing)
        self.assertTrue(context.exception)

    def test_map_letter(self):
        """
        Tests the map_letter method for an Enigma Plugboard.
        Performs a few test cases of mapping a letter through the
        reflector.
        """
        letter_inputs = ['A', 'B', 'G', 'Z']
        expected_outputs = ['M', 'B', 'G', 'W']
        for i in range(len(letter_inputs)):
            actual_output = self.plugboard.map_letter(letter_inputs[i])
            self.assertTrue(actual_output, expected_outputs[i])


class EnigmaMachineTestCase(unittest.TestCase):
    """
    Test case for an Enigma Plugboard.
    Methods tested:
        letter_to_number
        number_to_letter
        caeser_shift
        turn_rotor_assembly
        press_key
        encrypt_message

    Notes:
    __init__ not tested as it only calls previous __init__methods already
    tested.
    """
    def setUp(self):
        """
        Construct an Enigma Machine.
        """
        rotor_types = ['I', 'II', 'III']
        reflector_mapping = 'B'
        steckered_pairing = 'AM FI NV PS TU WZ'

        self.EnigmaMachine = \
            EnigmaMachine(rotor_types=rotor_types,
                          rotor_positions='DEF',
                          ring_settings='ABC',
                          reflector_mapping=reflector_mapping,
                          steckered_pairing=steckered_pairing)

    def test_letter_to_number(self):
        """
        Tests the letter_to_number method for an Enigma Machine.
        Performs a few test cases and that correct exceptions are raised.
        """
        letter_inputs = ['f', 'B', 'z']
        invalid_inputs = ['1', 1, 'AB']
        expected_outputs = [5, 1, 25]

        # Check valid inputs
        for i in range(len(letter_inputs)):
            actual_output = EnigmaMachine.letter_to_number(letter_inputs[i])
            self.assertTrue(actual_output, expected_outputs[i])

        # Check invalid inputs
        for letter in invalid_inputs:
            with self.assertRaises(ValueError) as context:
                EnigmaMachine.letter_to_number(letter)
            self.assertTrue(context.exception)

    def test_number_to_letter(self):
        """
        Tests the number_to_letter method for an Enigma Machine.
        Performs a few test cases and that correct exceptions are raised.
        """
        number_inputs = [0, 1, 10]
        invalid_inputs = ['1', 27, 'A']
        expected_outputs = ['A', 'B', 'K']

        # Check valid inputs
        for i in range(len(number_inputs)):
            actual_output = EnigmaMachine.number_to_letter(number_inputs[i])
            self.assertTrue(actual_output, expected_outputs[i])

        # Check invalid inputs
        for number in invalid_inputs:
            with self.assertRaises(ValueError) as context:
                EnigmaMachine.number_to_letter(number)
            self.assertTrue(context.exception)

    def test_caeser_shift(self):
        """
        Caeser shift of n moves a letter up the alphabet by n.
        Checks for invalid arguments.
        """
        letter_inputs = ['a', 'A', 'e']
        shift_inputs = [1, 4, 12]
        expected_outputs = ['B', 'E', 'Q']
        for i in range(len(letter_inputs)):
            actual_output = EnigmaMachine.caeser_shift(letter_inputs[i],
                                                       shift_inputs[i])
            self.assertEqual(expected_outputs[i], actual_output)

        invalid_inputs = [1, '2', 'dv']
        for letter in invalid_inputs:
            with self.assertRaises(ValueError) as context:
                EnigmaMachine.caeser_shift(letter, 1)
            self.assertTrue(context.exception)

    def test_turn_rotor_assembly(self):
        """
        Makes sure notch mechanism works correctly.
        """
        expected_positions = ['E', 'F', 'G']
        actual_positions = []
        self.EnigmaMachine.turn_rotor_assembly()
        for rotor in self.EnigmaMachine.rotors:
            actual_positions.append(rotor.position)
        self.assertEqual(expected_positions, actual_positions)

    def test_press_key(self):
        """
        Checks press_key inputs and outputs.
        """
        inputs = ['A', 'B', 'C']
        expected_outputs = ['N', 'L', 'S']
        actual_outputs = []
        for letter in inputs:
            actual_outputs.append(self.EnigmaMachine.press_key(letter))
        self.assertEqual(expected_outputs, actual_outputs)

    def test_encrypt_message(self):
        """
        Using this unit test as a bit of a smoke test.
        Encrypted message calculated from another virtual Enigma Machine.
        """
        expected_message = 'SRTMD'
        actual_message = self.EnigmaMachine.encrypt_message('HELLO')
        self.assertEqual(expected_message, actual_message)


if __name__ == '__main__':
    unittest.main()
