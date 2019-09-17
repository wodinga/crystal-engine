#!/usr/bin/env python3
import threading
import sys
import jack
import time
from mido import MidiFile
event = threading.Event()

class crystalengine:
    def __init__(self):
        self.synth = ['synthv1:out_1','synthv1:out_2']
        self.filename = '/home/pi/Aella.mid'
        self.connect_to = 'synthv1:in'
        self.sr = None  # sampling rate
        try:
            self.aella = iter(MidiFile(self.filename))
        except Exception as e:
            sys.exit(type(e).__name__ + ' while loading MIDI: ' + str(e))
        self.client = jack.Client('Crystal')
        self.playback = self.client.get_ports(is_audio=True, is_output=False, is_physical=True)
        self.midiOut = self.client.midi_outports.register('midiOut')
        @self.client.set_samplerate_callback
        def samplerate(samplerate):
            self.sr = samplerate

        @self.client.set_shutdown_callback
        def shutdown(status, reason):
            print('JACK shutdown:', reason, status)

        @self.client.set_process_callback
        def process(frames):
            self.midiOut.clear_buffer()
            offset = 0
            for note in self.aella:
                offset += round(note.time * self.sr)
                print(note)
                self.midiOut.write_midi_event(offset, note.bytes())

    def playSound(self):
        with self.client:
            if self.connect_to:
                self.midiOut.connect(self.connect_to)
                self.client.connect(self.synth[1], self.playback[1])
                self.client.connect(self.synth[0], self.playback[0])
                print('should be playing')
                try:
                    event.wait()
                except KeyboardInterrupt:
                    print('\nInterrupted by user')

engine = crystalengine()
engine.playSound()
