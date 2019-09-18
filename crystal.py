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
        self.offset = 0
        self.msg = next(self.aella)

        @self.client.set_samplerate_callback
        def samplerate(samplerate):
            self.sr = samplerate
            print(self.sr)

        @self.client.set_shutdown_callback
        def shutdown(status, reason):
            print('JACK shutdown:', reason, status)
            event.set()

        @self.client.set_process_callback
        def process(frames):
            midiOut = self.midiOut
            self.midiOut.clear_buffer()
            while True:
                if self.offset >= frames:
                    self.offset -= frames
                    return  # We'll take care of this in the next block ...
                # Note: This may raise an exception:
                self.midiOut.write_midi_event(self.offset, self.msg.bytes())
                #print(msg)
                try:
                    self.msg = next(self.aella)
                except StopIteration:
                    event.set()
                    raise jack.CallbackExit
                self.offset += round(self.msg.time * self.sr)



    def playSound(self):
        client = self.client
        synth = self.synth
        playback = self.playback
        with client:
            print(self.connect_to)
            if self.connect_to:
                self.midiOut.connect(self.connect_to)
            if len(client.get_all_connections(synth[0])) == 0:
                client.connect(synth[0], playback[0])
                client.connect(synth[1], playback[1])
                print('should be playing')
            print('Playing', repr(self.filename), '... press Ctrl+C to stop')
            try:
                event.wait()
            except KeyboardInterrupt:
                self.midiOut.clear_buffer()
                print('\nInterrupted by user')

engine = crystalengine()
engine.playSound()
