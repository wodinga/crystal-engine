#!/usr/bin/env python3
import sox
import threading
import keyboard

class crystalengine:
    def __init__(self):
        self.PODIUMS = {
            'red': 'sounds/Untitled 1-Sylenth1.wav',
            'blue': 'sounds/Untitled 2-Sylenth1.wav',
            'green': 'sounds/Untitled 3-Sylenth1.wav',
            'yellow': 'sounds/Untitled 4-Sylenth1.wav'
        }
        self.active_podiums = dict.fromkeys(self.PODIUMS, False)
        self.tfm = sox.Transformer()
        self.tfm.set_globals(verbosity=3) # for debugging
        self.comb = sox.Combiner()

    def activate_podiums(self, podium):
        if podium in self.active_podiums:
            self.active_podiums[podium] = True
            print(self.active_podiums)

    def toggle_podiums(self, podium):
        if podium in self.active_podiums:
            self.active_podiums[podium] = not self.active_podiums[podium]
            print(self.active_podiums)

    def deactivate_podiums(self, podium):
        if podium in self.active_podiums:
            self.active_podiums[podium] = False
            print(self.active_podiums)

    def play_sound(self):
        #Filter active_podiums to get only podiums set to True
        active_dict = {k: v for k,v in self.active_podiums.items() if v==True}
        #Get keys of active podiums
        keys = active_dict.keys()
        # Use keys to grab filenames
        files = list(map(lambda x: self.PODIUMS[x], keys)) # Contains list of audio files for active podiums
        # Grabs file extension and sets file_type
        self.comb.set_input_format(file_type=list(map(lambda file: file.split('.')[1], files)))
        print(active_dict)
        print(keys)
        for entry in files:
            print(entry)
        self.comb.preview(files, combine_type="merge")

crystal = crystalengine()

crystal.activate_podiums('green')
crystal.deactivate_podiums('yellow')
key = ''
while True:
    key = input()
    if key == '1':
        crystal.toggle_podiums('red')
    elif key == '2':
        crystal.toggle_podiums('blue')
    elif key == '3':
        crystal.toggle_podiums('green')
    elif key == '4':
        crystal.toggle_podiums('yellow')
    crystal.play_sound()
