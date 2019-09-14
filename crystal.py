#!/usr/bin/env python3
import sys
import threading

import jack
from mido import MidiFile

class crystalengine:
   def __init__(self):
    self.sr = None  # sampling rate
    self.client = jack.Client('Crystal')
    @self.client.set_samplerate_callback
    def samplerate(samplerate):
        self.sr = samplerate


    @self.client.set_shutdown_callback
    def shutdown(status, reason):
        print('JACK shutdown:', reason, status)
        event.set()

engine = crystalengine()
print(engine.sr)
