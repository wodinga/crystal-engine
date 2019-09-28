#!/usr/bin/env python3
import sox
import threading
import keyboard

class crystalengine:
    def __init__(self):
        self.PODIUM = {
            'red': 'Untitled 1-Sylenth1.wav',
            'blue': 'Untitled 2-Sylenth1.wav',
            'green': 'Untitled 3-Sylenth1.wav',
            'yellow': 'Untitled 4-Sylenth1.wav'
        }
        self.active_podiums = dict.fromkeys(self.PODIUM, False)
        self.tfm = sox.Transformer()

    def activatePodium(self, podium):
        if podium in self.active_podiums:
            self.active_podiums[podium] = True
            print(self.active_podiums)

    def deactivatePodium(self, podium):
        if podium in self.active_podiums:
            self.active_podiums[podium] = False
            print(self.active_podiums)

crystal = crystalengine()

crystal.activatePodium('red')
crystal.activatePodium('green')
crystal.deactivatePodium('green')
crystal.deactivatePodium('yellow')
