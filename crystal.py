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
        print(self.playback)
        self.midiOut = self.client.midi_outports.register('midiOut')
        @self.client.set_samplerate_callback
        def samplerate(samplerate):
            self.sr = samplerate

        @self.client.set_shutdown_callback
        def shutdown(status, reason):
            self.midiOut.clear_buffer()
            print('JACK shutdown:', reason, status)

        @self.client.set_process_callback
        def process(frames):
            self.midiOut.clear_buffer()
            offset = 0
            for note in self.aella:
                print(note)
                try:
                    self.midiOut.write_midi_event(offset, note.bytes())
                except Exception as e:
                    print(e)
                    raise jack.CallbackExit
                offset += round(note.time * self.sr)

    def playSound(self):
        client = self.client
        synth = self.synth
        playback = self.playback
        with client:
            self.midiOut.clear_buffer()
            if len(client.get_all_connections(synth[0])) == 0:
                client.connect(synth[0], playback[0])
                client.connect(synth[1], playback[1])
                print('should be playing')
                try:
                    event.wait()
                except KeyboardInterrupt:
                    print('\nInterrupted by user')
            if self.connect_to:
                self.midiOut.connect(self.connect_to)

engine = crystalengine()
engine.playSound()
