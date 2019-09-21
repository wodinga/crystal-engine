#!/usr/bin/env python3
#!/usr/bin/env python3
import threading
import _thread
import sys
import jack
import time
from mido import MidiFile
event = threading.Event()
synth = ['synthv1:out_1','synthv1:out_2']
synth2 = ['synthv1-01:out_1','synthv1-01:out_2']
synth3 = ['synthv1-02:out_1','synthv1-02:out_2']

midiIn = 'synthv1:in'
midiIn2 = 'synthv1-01:in'
midiIn3 = 'synthv1-02:in'

midiOut = 'synthv1:in'
midiOut2 = 'synthv1-01:out'
midiOut3 = 'synthv1-02:out'

crystal = 'crystal'
crystal2 = 'crystal2'
crystal3 = 'crystal3'
class crystalengine:
    def __init__(self, s=['synthv1:out_1','synthv1:out_2'],
    m='synthv1:in',
    o ='synthv1:out',
    c='Crystal'):
        self.filename = '/home/pi/Aella.mid'
        self.synth = s
        self.connect_to = m
        self.sr = None  # sampling rate
        try:
            self.aella = iter(MidiFile(self.filename))
        except Exception as e:
            sys.exit(type(e).__name__ + ' while loading MIDI: ' + str(e))
        self.client = jack.Client(c)
        self.playback = self.client.get_ports(is_audio=True, is_output=False, is_physical=True)
        self.midiOut = self.client.midi_outports.register(o)
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
        print('balls')
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
                client.cpu_load()
                print('should be playing')
            print('Playing', repr(self.filename), '... press Ctrl+C to stop')
            try:
                event.wait()
            except KeyboardInterrupt:
                self.midiOut.clear_buffer()
                print('\nInterrupted by user')

engine = crystalengine(synth, midiIn, crystal)
#engine2 = crystalengine(synth2, midiIn2, crystal3)
engine3 = crystalengine(synth3, midiIn3, crystal2)
print('start thread 1')
_thread.start_new_thread(engine.playSound, ())
print('start thread 2')
_thread.start_new_thread(engine3.playSound, ())
event.wait()
