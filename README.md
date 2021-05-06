
# Enigma Machine Simulator

Python implementation of the Enigma machine, an encryption device used by the German military in WWII.
https://en.wikipedia.org/wiki/Enigma_machine

Thought unbreakable, Polish and British codebreakers were able to crack the code and in so doing, led to the creation of the world's first computers.

## How to run the simulator
```shell
git clone https://github.com/gareth-case/Enigma.git
cd Enigma
python enigma_machine.py
```

## Learn a bit about how Enigma works

There is a .ipynb notebook that explores the constituent parts of the Enigma machine and decrypts some real world messages sent using the machine.

## Build your own machine

You import the enigma_machine module to craft your own machine and play with the pieces.

```python
from enigma_machine import EnigmaMachine
# Initialise Enigma Machine
EM = EnigmaMachine(rotor_types=['I', 'II', 'III'],  
                   ring_settings='AAA',
                   rotor_positions='AAA',
                   reflector_mapping='B',
                   steckered_pairing='AB CD EF'
                   )

# Encrypt message
EM.encrypt_message('A really cool message')
```

