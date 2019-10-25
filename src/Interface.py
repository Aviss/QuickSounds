from threading import Timer
import time
import sys
import keyboard as kb

from src.sounds.Overlay import Overlay
from src.sounds.SoundStream import SoundStream
from src.config.Configuration import resolveSoundByName, updateConfig, handleError, SILENCE, resolveSoundByStrokes, config
from src.config.ConfigNames import *

class Interface:
    def __init__(self):

        self.soundboardActive = True

        self.acceptHotkeys = True
        self.modifierPressed = False
        self.lastHotBarButton = None
        self.overlayTimer = None
        
        self.lastCancelPress = 0
        self.isCancelPressed = False

        self.lastReloadPress = 0
        self.isReloadPressed = False

        self.overlay = Overlay()
        self.outputStreams = []

        self.reload()

        kb.on_press(self.keyPressed)
        kb.on_release(self.keyReleased)

        # Can only be stopped by destroying overlay        
        self.overlay.mainloop()

    """ Create new stream to play sound and immediately """
    def playOneShotSound(self, device, sound):
        ss = SoundStream(device)
        self.outputStreams.append(ss)

        ss.changeSound(sound)
        ss.stopGracefully()

        return ss
    
    def playGlobal(self, sound):
        for device in [config(HEADPHONES), config(MICROPHONE)]:
            self.playOneShotSound(device, sound)

    def playNotification(self, sound):
        self.playOneShotSound(config(HEADPHONES), sound)

    def stopPlayback(self):
        for stream in self.outputStreams:
            stream.kill()
        self.outputStreams = []

    def toggleSoundboardActive(self):
        self.soundboardActive = not self.soundboardActive
        if self.soundboardActive:
            self.playNotification(resolveSoundByName(ENABLE_SOUND))
        else:
            self.playNotification(resolveSoundByName(DISABLE_SOUND))

    def shutDown(self):
        self.acceptHotkeys = False
        self.stopPlayback()
        self.playNotification(resolveSoundByName(SHUTDOWN_SOUND))

        # Wait for shutdown sound to complete
        for stream in self.outputStreams:
            stream.waitForCompletion()

        # Destroy overlay, therefore ending the mainloop
        if self.overlay:
            self.overlay.destroy()

    def reload(self):
        try:
            updateConfig()

            self.overlay.tryUpdate()

            try:
                # Just test Stream initialization
                self.playGlobal(SILENCE)
            except Exception as e:
                s = "Error Occurred during Stream Initialization.\n"
                s += str(e) + "\n\n"

                s += "Make sure you chose the correct devices"

                raise RuntimeError(s)
        except Exception as e:
            handleError(str(e))
            self.shutDown()
            sys.exit(0)

        self.playNotification(resolveSoundByName(READY_SOUND))

    """ As long as an event is still being processed, all other key presses are put in a queue"""
    def keyPressed(self, e):
        # Due to the queue nature of the events, this switch can only be used from outside
        if self.acceptHotkeys:
            if kb.matches(e, config(MODIFY_KEY)):
                self.modifierPressed = True
                
            elif kb.matches(e, config(TOGGLE_ACTIVE_KEY)) and self.modifierPressed:
                self.toggleSoundboardActive()
                
            elif kb.matches(e, config(CANCEL_KEY)):
                self.invalidateHotkey()
                self.stopPlayback()
                if not self.isCancelPressed:
                    self.lastCancelPress = e.time
                    self.isCancelPressed = True
                else:
                    if self.lastCancelPress + config(LONG_HOLD_TIME) < e.time:
                        self.shutDown()
                        
            elif kb.matches(e, config(RELOAD_KEY)):
                if not self.isReloadPressed:
                    self.lastReloadPress = e.time
                    self.isReloadPressed = True
                else:
                    if self.lastReloadPress + config(LONG_HOLD_TIME) < e.time:
                        self.stopPlayback()
                        self.playNotification(resolveSoundByName(RELOAD_SOUND))
                        self.reload()
                        # Reset countdown to reload
                        # Don't use event time here. Significant time has passed
                        self.lastReloadPress = time.time()

            # Handle choosing of sounds
            elif e.name in config(HOTBAR_KEYS) and self.modifierPressed and self.soundboardActive:
                if self.lastHotBarButton is not None:
                    self.playGlobal(resolveSoundByStrokes(config(HOTBAR_KEYS)[self.lastHotBarButton.name], config(HOTBAR_KEYS)[e.name]))
                    self.invalidateHotkey()
                else:
                    self.lastHotBarButton = e
                    self.overlay.drawOverlay(config(HOTBAR_KEYS)[e.name])
                    self.overlayTimer = Timer(config(OVERLAY_STAY_DURATION), self.invalidateHotkey)
                    self.overlayTimer.start()

    """ Reset Hotkey state. Two new hotkeys need to be pressed to trigger a sound """
    def invalidateHotkey(self):
        self.lastHotBarButton = None
        if self.overlay:
            self.overlay.hideOverlay()
        if self.overlayTimer:
            self.overlayTimer.cancel()

    def keyReleased(self, e):
        if e.name == config(MODIFY_KEY):
            self.modifierPressed = False
        if kb.matches(e, config(CANCEL_KEY)):
            self.isCancelPressed = False
        if kb.matches(e, config(RELOAD_KEY)):
            self.isReloadPressed = False