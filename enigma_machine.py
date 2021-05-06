# -*- coding: utf-8 -*-
"""Enigma Machine Simulator.

This module is a Python implementation of the Enigma Machine.

Ran as a script it starts a simulation and allows a user to configure and use
their own Enigma Machine.
"""

import string
from time import sleep


class EnigmaMachine:
    """
    A class to represent an Enigma Machine.
    It comprises a set of rotors (usually three), a reflector, and an optional
    plugboard.


    Attributes
    ----------
    rotors : lst
        List of Enigma Rotors (list of EnigmaMachine.Rotor() object)
    plugboard : EnigmaMachine.Plugboard()
        Plugboard object
    reflector : EnigmaMachine.Reflector()
        Reflector object
    """
    def __init__(self,
                 # Standard Rotors for the Enigma I machine
                 rotor_types=['I', 'II', 'III'],
                 rotor_positions='DEF',
                 ring_settings='ABC',
                 reflector_mapping='B',
                 steckered_pairing='AM FI NV PS TU WZ'):
        """
        Initialises an EnigmaMachine with rotors, reflector and plugboard.
        Args:
            rotor_types (lst): List of types of rotor in the machine
            rotor_positions (str): Initial positions of the rotors
            ring_settings (str): Ring settings of the rotors
            reflector_mapping (str): Requesite information to initialise a
                                     EnigmaMachine.Reflector object
            steckered_pairing (str): Requesite information to initialise a
                                     EnigmaMachine.Plugboard object. If False
                                     then plugboard is set at "ABCDE..."
                                     (which is equivalent to no plugboard).
        """
        # Initialise rotors from config.
        if len(rotor_types) != len(ring_settings):
            raise ValueError('Number of ring settings must match with number '
                             'of rotors')
        elif len(rotor_types) != len(rotor_positions):
            raise ValueError('Number of rotor positions must match with '
                             'number of rotors')
        self.rotors = []
        for i in range(len(rotor_types)):
            self.rotors.append(EnigmaMachine.Rotor(
                rotor_type=rotor_types[i],
                position=rotor_positions[i],
                ring_setting=ring_settings[i]))
        # Provides the option of having no plugboard
        if not steckered_pairing:
            steckered_pairing = ''
        self.plugboard = EnigmaMachine.Plugboard(steckered_pairing)
        self.reflector = EnigmaMachine.Reflector(reflector_mapping)

    def __repr__(self):
        """
        String representation of an EnigmaMachine used for debugging.
        """
        return (f'EnigmaMachine(rotors={self.rotors}, '
                f'plugboard={self.plugboard}, reflector={self.reflector}, '
                f'rotor_config={self.rotor_config})')

    def __str__(self):
        """
        String representation of an EnigmaMachine used for printing to console.
        """
        if self.plugboard.steckered_pairing == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            pb_str = 'no plugboard'
        else:
            pb_str = 'a plugboard'
        return (f'Enigma Machine with {len(self.rotors)} rotors, a reflector'
                f' and {pb_str}.')

    @staticmethod
    def letter_to_number(letter):
        """
        Converts a letter to its integer in the alphabet from 0 to 25.
        Arguments:
            letter (str): Letter to convert.

        Returns:
            number (int): Integer between 0 and 25 corresponding to letter's
                          place in the alphabet.

        Raises:
            ValueError if input is not a letter.
        """
        if type(letter) != str:
            raise ValueError('Input not a string')
        if not letter.isalpha() or len(letter) != 1:
            raise ValueError('Input should be a single letter')
        letter = str.upper(letter)
        number = string.ascii_uppercase.index(letter)

        return number

    @staticmethod
    def number_to_letter(number):
        """
        Finds the letter from the alphabet corresponding to number.

        Example: number_to_letter(0) = 'A'

        Arguments:
            number (int): Place in alphabet of letter to find.

        Returns:
            letter (int): Upper case letter of alphabet.

        Raises:
            ValueError if input is not a number between 0 and 25.
        """
        if type(number) != int or not 0 <= number < 26:
            raise ValueError('Input should be an integer between 0 and 25')

        letter = chr(number + 65)

        return letter

    @staticmethod
    def caeser_shift(letter, n):
        """
        Shifts a letter up the alphabet by n. (Known as a "Caeser Shift").

        Example: caeser_shift('L', 2) = 'N'

        Arguments:
            letter (str): Letter to transpose.
            n (int): Number of places to shift by.

        Returns:
            shifted_letter (int): Letter after Caeser Shift has been performed.

        Raises:
            ValueError if input is not a letter.
        """
        if type(letter) != str:
            raise ValueError('Input should be a string')
        elif not (letter.isalpha() and len(letter) == 1):
            raise ValueError('Input should be a single letter')

        letter = str.upper(letter)
        shifted_letter = chr((ord(letter) - 65 + n) % 26 + 65)
        return shifted_letter

    def turn_rotor_assembly(self):
        """
        Turns the rotor assembly as a whole. This is performed by firstly
        rotating the right-most rotor one place. The other rotors are then
        rotated if the rotor to their immediate right was in its "notch"
        position. This is calcuated for each rotor in the assembly.

        Example: Rotor 1 has position 'A' and notch at 'G'
                 Rotor 2 has position 'B' and notch at 'H'
                 Rotor 3 has position 'E' and notch at 'E'

        Then Rotor 3 is turned automatically, but as it was in its notch
        position (notch == position) then Rotor 2 is also turned. Rotor 1 is
        not turned because Rotor 2 was not at its notch position.
        """
        for i in range(len(self.rotors) - 1):
            rotor = self.rotors[i]
            adjacent_rotor = self.rotors[i + 1]
            if adjacent_rotor.notch == adjacent_rotor.position:
                rotor.turn_rotor()
                if i < len(self.rotors) - 2:
                    adjacent_rotor.turn_rotor()

        # Last rotor always turns
        self.rotors[-1].turn_rotor()

    def press_key(self, letter):
        """
        Emulates the pressing of a key on the Enigma keyboard. Every time a
        key is pressed, the rotor assembly is turned. This is one of the key
        properties of the EnigmaMachine.

        Arguments:
            letter (str): Letter pressed.

        Returns:
            encrypted_letter (str): The letter that would be lit on the Enigma
            lampboard. after pressing the "letter" key.
            (In other words, what "letter" was encrypted to).

        Raises:
            ValueError if input is not a letter of length one.
            (You can't press two keys at once otherwise you'll be disciplined
            by your senior officer in the Wehrmacht!).
        """
        if type(letter) != str or len(letter) != 1:
            raise ValueError

        # As soon as a letter is pressed, the rotor assembly turns.
        self.turn_rotor_assembly()

        # The first stage is the current goes through the plugboard.
        encrypted_letter = self.plugboard.map_letter(letter)

        encrypted_letter = encrypted_letter
        # The current flows through the rotors in reverse order to begin with
        # (so right-most rotor first moving leftwards).
        for rotor in reversed(self.rotors):
            encrypted_letter = rotor.map_letter(encrypted_letter)

        # Current now passes through the reflector.
        encrypted_letter = self.reflector.map_letter(encrypted_letter)
        # Current now passes back through the rotors, but starting from the
        # left this time (so rotor 1 -> rotor 2 -> rotor 3...)
        for rotor in self.rotors:
            encrypted_letter = rotor.map_letter(encrypted_letter,
                                                reverse=True)

        # Current finally flows back through the plugboard and lights up a
        # character to show you the encrypted letter. Exciting!
        encrypted_letter = self.plugboard.map_letter(encrypted_letter)
        return encrypted_letter

    def encrypt_message(self, message):
        """
        Encrypts a message using the EnigmaMachine by consecutively pressing
        each key of the message to be encrypted. It skips any characters that
        aren't alphabetical such as punctuation, numbers etc.

        Arguments:
            message (str): Message to be encrypted.

        Returns:
            encrypted_message (str): The encrypted message.

        Raises:
            ValueError if input is not a string.
        """
        if type(message) != str:
            raise ValueError

        encrypted_message = ''

        for letter in message:
            if letter.isalpha():
                encrypted_message = encrypted_message + self.press_key(letter)

            else:
                encrypted_message = encrypted_message + letter

        return encrypted_message

    class Rotor:
        """
        A class to represent an Enigma Rotor.
        A rotor has a letter mapping, a position, a ring setting and a notch.

        The letter mapping is essentially the internal wiring of the rotor, it
        tells you which letter is mapped to which.

        The position is one of 26 rotary positions of the rotor in the machine.
        If you turn the rotor, then this position is changed.

        Ring settings are similar to the position, but they affect the position
        of the internal wiring of the rotor, relative to the rotor itself.

        The notch is a mechanical device which can turn the rotor immediately
        to the left of this rotor.

        Attributes:
            rotor_type: (str)
                A Roman Numeral expressing the rotor type (I-V).
            position: (str)
                A letter of the alphabet denoting the position of the rotor.
            ring_setting: (str)
                A letter of the alphabet denoting the ring setting of the
                rotor.
            notch: (str)
                A letter of the alphabet denoting the position of the notch
                of the rotor.
        """
        def __init__(self, rotor_type='I', position='A', ring_setting='A'):
            """
            Initialises a Rotor from an EnigmaMachine. Also updates the mapping
            with the appropriate shift from the rotor's ring setting.
            Args:
                mapping: (str)
                A string of length 26 that says what each letter is mapped to.
                position: (str)
                    A letter of the alphabet denoting the position of the
                    rotor.
                ring_setting: (str)
                    A letter of the alphabet denoting the ring setting of the
                    rotor.
                notch: (str)
                    A letter of the alphabet denoting the position of the notch
                    of the rotor.
            Raises:
                ValueError if mapping is not a valid alphabet mapping.
                ValueError if any other attribute is not an alphabetic
                character of length one
            """
            if rotor_type == 'I':
                self.mapping = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
                self.notch = 'Q'
            elif rotor_type == 'II':
                self.mapping = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
                self.notch = 'E'
            elif rotor_type == 'III':
                self.mapping = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
                self.notch = 'V'
            elif rotor_type == 'IV':
                self.mapping = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
                self.notch = 'J'
            elif rotor_type == 'V':
                self.mapping = 'VZBRGITYUPSDNHLXAWMJQOFECK'
                self.notch = 'Z'
            else:
                raise ValueError('Must choose a rotor type I - V')
            self.position = position
            self.ring_setting = ring_setting
            for rotor_item in [position, ring_setting]:
                if type(rotor_item) != str:
                    raise ValueError('Attribute must be a string')
                elif not rotor_item.isalpha():
                    raise ValueError('Attribute must be alphabetic')
                elif len(rotor_item) != 1:
                    raise ValueError('Attribute must have length 1')
            # Apply the ring setting to the rotor which changes its mapping.
            self.apply_ring_setting(ring_setting)

        def __str__(self):
            """
            String representation of a Rotor used for printing to console.
            """
            return (f'A Rotor for an Enigma Machine with letter mapping "'
                    f'{self.mapping}", ring setting "{self.ring_setting}", '
                    f'position "{self.position}", and a '
                    f'notch at position "{self.notch}"')

        def turn_rotor(self):
            """
            Turns the rotor.
            Example: If a rotor is in position "F" then after turning
                     it will be in position "G".
            """
            # Translate letter position to number
            position_nbr = EnigmaMachine.letter_to_number(self.position)
            # Get new letter position by adding 1
            new_rotor_nbr = (position_nbr + 1) % 26
            self.position = EnigmaMachine.number_to_letter(new_rotor_nbr)

        def apply_ring_setting(self, letter):
            """
            The ring setting (or Ringstellung) changes the internal wiring of
            the rotor.
            All letters in the mapping are shifted by the number corresponding
            to the ring setting.

            Example: rotor.apply_ring_setting('A') would have no effect on the
            rotor (as A->0).
            rotor.apply_ring_setting('B') would perform a Caeser shift by 1 to
            each letter in rotor.mapping (so "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            becomes "FLNGMHERWAOUPVZIYWTQBJCSDK").
            """
            shift = EnigmaMachine.letter_to_number(letter)
            shifted_mapping = ''
            for letter in self.mapping:
                shifted_mapping = shifted_mapping + \
                                  EnigmaMachine.caeser_shift(letter, shift)
            # Adding positional shift due to ring settings
            shifted_mapping = [char for char in shifted_mapping]
            shifted_mapping = \
                [shifted_mapping[(i - shift) % 26] for i in range(26)]

            self.mapping = "".join(shifted_mapping)

        def map_letter(self, letter, reverse=False):
            """
            Given a letter input, finds the letter it would be mapped to
            through the rotor wiring. Takes into account the rotor position
            as well as the underlying mapping. Can also do the reverse of this
            for when the current passes back through the rotor.

            Arguments:
                letter (str): Letter to be mapped.
                reverse (bool): Whether the current is going in reverse back
                                through the rotor. It does this after it goes
                                through the reflector.

            Returns:
                mapped_letter (str): Resulting letter after passing through
                                     the rotor wiring.

            Raises:
            ValueError if input is not a string of length 1.
            """
            if type(letter) != str or len(letter) != 1:
                raise ValueError
            letter = str.upper(letter)
            # Add the transformation due to the rotor position.
            initial = EnigmaMachine.letter_to_number(self.position)
            if reverse:
                letter = EnigmaMachine.caeser_shift(letter, initial)
                mapped_letter = EnigmaMachine.number_to_letter((
                    self.mapping.index(letter) - initial) % 26)

            else:
                position = \
                   (initial + EnigmaMachine.letter_to_number(letter)) % 26
                # Take into account the offset caused by the rotor being in
                # a different position.
                mapped_letter = \
                    EnigmaMachine.caeser_shift(self.mapping[position],
                                               -initial)
            return mapped_letter

    class Reflector:
        """
        A class to represent an Enigma Reflector.
        The reflector pairs up two letters and is used in between the first and
        second rotor passes.

        The reflector enables the same Enigma machine to both encrypt and
        decrypt messages without having to change any settings, however also
        raises a key cryptographic weakness that the cryptoanalysts at
        Bletchley Park were able to exploit.

        Attributes:
            reflector_mapping: (str)
                A string of length 26 that says what each letter is mapped to.
                A mapping must pair up letters (so if A -> Y, then Y-> A).
                Can also be one of three standard reflectors (A, B or C).
        """
        def __init__(self, reflector_mapping='A'):
            """
            Initialises a Reflector from an EnigmaMachine.
            Args:
                reflector_mapping (str):
                    'A', 'B' or 'C' which correspond to the respective standard
                    reflectors used in the Enigma Machine.
                    Can alternativelybe a string of length 26 that says which
                    each letter is mapped to.
                    A mapping must pair up letters (so if A -> Y, then
                    Y-> A).

            Raises:
                ValueError if mapping does not map letter pairs.
            """
            if reflector_mapping.upper() == 'A':
                self.reflector_mapping = 'EJMZALYXVBWFCRQUONTSPIKHGD'
            elif reflector_mapping.upper() == 'B':
                self.reflector_mapping = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
            elif reflector_mapping.upper() == 'C':
                self.reflector_mapping = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
            else:
                self.reflector_mapping = reflector_mapping
            if type(self.reflector_mapping) != str or \
               len(set(self.reflector_mapping)) != 26:
                raise ValueError('Invalid reflector mapping')

            for i in range(len(self.reflector_mapping)):
                if EnigmaMachine.letter_to_number(self.reflector_mapping[i]) \
                    != self.reflector_mapping.index(
                        EnigmaMachine.number_to_letter(i)):
                    raise ValueError('Reflector must have matching pairs, '
                                     f'check letter '
                                     f'"{self.reflector_mapping[i]}"')

        def __str__(self):
            """
            String representation of a Reflector used for printing to console.
            """
            return (f'A reflector for an Enigma Machine with mapping'
                    f' "{self.reflector_mapping}".')

        def map_letter(self, letter):
            """
            Gives the corresponding letter pair of a reflector.

            Arguments:
                letter (str): Letter to be mapped.

            Returns:
                mapped_letter (str): Resulting letter after passing through
                                     the reflector.

            Raises:
            ValueError if input is not a string of length 1.
            """
            if type(letter) != str or len(letter) != 1:
                raise ValueError('Input must be a single character.')
            letter = str.upper(letter)

            position = EnigmaMachine.letter_to_number(letter) % 26
            mapped_letter = self.reflector_mapping[position]
            return mapped_letter

    class Plugboard:
        """
        A class to represent an Enigma Plugboard.
        The plugboard gives another layer of encryption to the Enigma Machine.
        It connects (usually 10) pairs of letters and this pairing is done
        at both the beginning and end of the encryption mechanism. The pairing
        is called a "steckered pairing" (from the German word for plugboard
        "Steckerbrett".)

        Without the plugboard, it was feasible to break the Enigma code using
        calculations by hand. With the introduction of the plugboard,
        cryptoanalysts needed the use of the earliest computers to help crack
        the code.

        Attributes:
            steckered_pairing: (str)
                A string of pairs of letters delimited by a space that encodes
                letter pairing.
        """
        def __init__(self, steckered_pairing='AM FI NV PS TU WZ'):
            """
            Initialises a Plugboard from an EnigmaMachine.
            Args:
                reflector_mapping (str):
                    A string of pairs of letters delimited by a space that
                    encodes letter pairing.

            Raises:
                ValueError if mapping does not map letter pairs.
            """
            self.steckered_pairing = steckered_pairing
            error = ('Steckered pairing must be unique pairs of letters '
                     'seperated by a space.')
            if type(steckered_pairing) != str:
                raise ValueError(error)
            steckered_pairing_no_spaces = steckered_pairing.replace(' ', '')
            # Needs to only be letters.
            if steckered_pairing != '':
                if not steckered_pairing_no_spaces.isalpha() \
                    or len(steckered_pairing) % 3 != 2 \
                    or len(set(steckered_pairing_no_spaces)) != \
                        len(steckered_pairing_no_spaces):
                    raise ValueError(error)
                # needs to be pairs of letters
                for i in range(len(steckered_pairing)):
                    if i % 3 == 2 and steckered_pairing[i] != ' ':
                        raise ValueError(error)
                    elif i % 3 != 2 and not steckered_pairing[i].isalpha():
                        raise ValueError(error)

        def __str__(self):
            return (f'A plugboard for an Enigma Machine with steckered '
                    f'pairing "{self.steckered_pairing}".')

        def map_letter(self, letter):
            """
            Gives the corresponding letter pair of a plugboard.

            Arguments:
                letter (str): Letter to be mapped.

            Returns:
                mapped_letter (str): Resulting letter after passing through
                                     the plugboard.

            Raises:
            ValueError if input is not a string of length 1.
            """
            if type(letter) != str or len(letter) != 1:
                raise ValueError
            letter = str.upper(letter)
            pairing = self.steckered_pairing
            if letter not in pairing:
                mapped_letter = letter
            else:
                position = pairing.index(letter)
                if pairing.index(letter) == len(pairing) - 1:
                    mapped_letter = pairing[position - 1]
                elif pairing[position + 1] == ' ':
                    mapped_letter = pairing[position - 1]
                else:
                    mapped_letter = pairing[position + 1]

            return mapped_letter


if __name__ == '__main__':
    print('Welcome to the Enigma Simulator!')
    sleep(2)
    print('Here you can configure very own Enigma Machine and use it to '
          'encrypt messages.')
    configure_enigma = input('Enter Y to skip configuration and use default '
                             'settings or instead enter any key to go ahead '
                             'and configure your machine. ')
    if str.upper(configure_enigma) == 'Y':
        print('Default machine selected.')
        EM = EnigmaMachine()
    else:
        print('Time to configure the machine!')
        num_rotor = int(input('Firstly, enter the number of rotors in your '
                              'machine: '))
        rotor_types = []
        rotor_positions = ''
        ring_settings = ''
        for i in range(num_rotor):
            print(f'Let\'s configure rotor {i+1}')
            rotor_type = input(f'Enter the rotor type (Roman numeral I - V) '
                               f' for rotor {i+1}: ')
            rotor_types.append(rotor_type)

            rotor_position = str.upper(input(
                f'Enter the rotor position (single letter A-Z) for rotor '
                f' {i+1}: '))
            rotor_positions = rotor_positions + rotor_position

            ring_setting = str.upper(input(
                f'Enter the ring setting  (single letter A-Z) for rotor {i+1}'
                ': '))
            ring_settings = ring_settings + ring_setting
        reflector_mapping = str.upper(input('Enter a reflector (A, B or C): '))
        steckered_pairing = str.upper(input(
            'Finally, enter a steckered pairing (pairs of letters or N for no'
            ' plugboard): '))
        EM = EnigmaMachine(rotor_types=rotor_types,
                           rotor_positions=rotor_positions,
                           ring_settings=ring_settings,
                           steckered_pairing=steckered_pairing,
                           reflector_mapping=reflector_mapping)
    print('Setting up machine...')
    sleep(1)
    print('Adjusting the rotors...')
    sleep(1)
    print('Pairing up the plugboard...')
    sleep(1)
    print('Your Enigma Machine is ready to use!')
    sleep(1)
    encryption = 'Y'
    while encryption == 'Y':
        message = input('Enter message to encrypt: ')
        print('Encrypting message...')
        sleep(1)
        print(f'Encrypted message: {EM.encrypt_message(message)}')
        encryption = str.upper(input(
            'Would you like to encrypt another message? (Y/N) '))

    print('Thanks for using the Enigma Simulator!')
