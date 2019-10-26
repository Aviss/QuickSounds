import sounddevice as sd
from threading import Lock

DEFAULT_SOUND_STREAM_PARAMETERS = {
    "samplerate": 44100,
    "dtype": "float32"
}

class SoundStream:
    def __init__(self, aDevice):

        self.device = aDevice

        self.timestamp = 0
        self.currentSoundData = None
        self.soundLock = Lock()

        # Immediately lock and only release when stream has stopped so that other threads can wait for completion
        self.lock = Lock()
        self.lock.acquire()
        self.killed = False

        self.stream = sd.OutputStream(device=self.device,
                                      callback=self.callback,
                                      finished_callback=self.releaseLock,
                                      **DEFAULT_SOUND_STREAM_PARAMETERS)
        self.stream.start()

    """
        Callback from OutputStream.
        - Sound to be played is written to outdata
        - frames tells us how much data should be played (static, determined by samplerate)
        - We use our own timestamp to allow playing sounds from the beginning (f.e. if sound changed)
        - status is only needed if something went wrong
    """
    def callback(self, outdata, frames, timestamp, status):
        # Don't allow sound to be changed while data is written to out
        self.soundLock.acquire()

        start = frames * self.timestamp
        self.timestamp += 1

        if self.currentSoundData is not None:
            # Check for end of sound
            stop = min(start + frames, len(self.currentSoundData))

            # Fill outdata with empty data in case of sound ending early
            outdata[:stop-start] = self.currentSoundData[start:stop] * 0.5
            if stop-start < frames:
                outdata[stop-start:, :].fill(0)
                self.currentSoundData = None
        else:
            # If we are not playing a sound, play silence
            outdata[:, :].fill(0)

        self.soundLock.release()

        # Always play current sound to completion before exiting
        if self.currentSoundData is None and self.killed:
            raise sd.CallbackStop

    def changeSound(self, sound):
        # Don't accept sound changes after stream has been killed
        if not self.killed:
            self.soundLock.acquire()
            self.timestamp = 0
            self.currentSoundData = sound.audioData
            self.soundLock.release()

    """ Only tell stream to not accept new sounds, finish playing current sound, then exit."""
    def stopGracefully(self):
        self.killed = True

    """ Stop playing current sound then exit """
    def kill(self):
        self.soundLock.acquire()
        self.currentSoundData = None
        self.killed = True
        self.soundLock.release()

    def releaseLock(self):
        self.lock.release()

    def waitForCompletion(self):
        self.lock.acquire()