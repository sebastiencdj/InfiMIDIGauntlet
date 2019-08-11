import argparse
from time import sleep

import socketio
from flask import Flask, render_template
from threading import Thread, Event
# noinspection PyPackageRequirements
import rtmidi
import wsgiserver

sio = socketio.Server(async_mode='threading')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

thread = Thread()
thread_stop_event = Event()


class MIDIThread(Thread):
    def __init__(self):
        super(MIDIThread, self).__init__()

    def get_and_send_codes(self):
        midiin = rtmidi.MidiIn()
        midiin.open_port(args.midi_device)
        while True:
            m = midiin.get_message()
            if m:
                sio.emit('code', {'code': m[0], 'since_last': m[1]}, namespace='/speedometer')
            sleep(0.001)

    def run(self):
        self.get_and_send_codes()


@app.route('/speedometer')
def index():
    return render_template('speedometer.html')


@sio.on('connect', namespace='/speedometer')
def connect(a, b):
    global thread
    if not thread.isAlive():
        thread = MIDIThread()
        thread.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gather the power of your MIDI devices with the InfiMIDI Gauntlet')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list-devices', action='store_true', help='List available MIDI devices')
    group.add_argument('-m', '--midi-device', type=int, help='Selected MIDI device (required)')
    args = parser.parse_args()
    if args.list_devices:
        midiin = rtmidi.MidiIn()
        ports = range(midiin.get_port_count())
        if ports:
            for i in ports:
                print('#' + str(i) + ': ' + midiin.get_port_name(i)[:-2])
    elif args.midi_device is not None:
        wsgiserver.WSGIServer(app, host='0.0.0.0', port=80).start()

