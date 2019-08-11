Install libraries with:
    python -m ensurepip --upgrade
    pip install -r requirements.txt
    
List devices with:
    python InfiMIDIGauntlet.py -l
    
Then select desired device and start server:
    python InfiMIDIGauntlet.py -m [number]
    
You can display the speedometer at http://[address]/speedometer
[address] is 127.0.0.1 if you access it from the same machine