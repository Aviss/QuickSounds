import re
import os
import soundfile as sf
import logging
import numpy as np
from PIL import Image
from sounddevice import query_devices as getDeviceInfo
from src.config.ConfigNames import *

class Sound:
    def __init__(self, audioData = None, image = None, label = None):
        self.audioData = audioData
        self.image = image
        self.label = label
SILENCE = Sound()

LOGGER = logging.getLogger('QuickSounds')
LOGGER.setLevel(logging.ERROR)

# Static configuration
ERROR_FILE_VALUE = "error.log"
CONFIG_FILE_VALUE = "cfg.ini"

MODIFY_KEY_VALUE = "alt gr"   # 69
FILTER_STREAM_KEY = "insert"
HOTBAR_KEYS_VALUE = {
    "end":          0, # 79
    "down":         1, # 80
    "page down":    2, # 81
    "left":         3, # 75
    "clear":        4, # 76
    "right":        5, # 77
    "home":         6, # 71
    "up":           7, # 72
    "page up":      8  # 73
}

# Dynamic maps #WhatIsRAM?
SYSTEM_SOUNDS = None
SOUNDS_BY_STROKES = None
CONFIG = None

def initConfig():
    global CONFIG
    CONFIG = {
        PUBLIC_DEVICE: None,
        PRIVATE_DEVICE: None,
        SOUND_PATH: None,
        RESOURCE_PATH: None,
        OVERLAY_MODE: "labels",

        RELOAD_SOUND : "reload.wav",
        ENABLE_SOUND : "enable.wav",
        DISABLE_SOUND : "disable.wav",
        SHUTDOWN_SOUND : "shutdown.wav",
        READY_SOUND : "ready.wav",

        OVERLAY_LABELS : "overlay.png",
        OVERLAY_IMAGES : "overlayImages.png",

        CANCEL_KEY : "num lock",  # 541
        RELOAD_KEY : "scroll lock",  # 70
        TOGGLE_ACTIVE_KEY : "-",  # 74
        OVERLAY_STAY_DURATION : 3,
        LONG_HOLD_TIME : 1,

        SOUND_IMAGE_EDGE_LENGTH : 100
    }

def updateConfig():
    global CONFIG
    initConfig()
    try:
        configFile = open(CONFIG_FILE_VALUE, "r")
        for line in configFile:
            tokens = line.split()

            if len(tokens) <= 0:
                continue

            if tokens[0].startswith("#"):
                continue

            if tokens[0] in CONFIG and len(tokens) > 1:
                CONFIG[tokens[0]] = ' '.join(tokens[1:])

    except Exception as e:
        s = "Error reading config file '{}':\n".format(CONFIG_FILE_VALUE)
        s += str(e) + "\n\n"

        s += "Make sure the '{}' is in the same folder as the exe.\n".format(CONFIG_FILE_VALUE)

        raise RuntimeError(s)

    try:
        processSounds()

    except Exception as e:
        s = "Error Loading sounds:\n"
        s += str(e) + "\n\n"

        if config(SOUND_PATH) is None or config(RESOURCE_PATH) is None:
            s += "It looks like you haven't specified a resources and/or a sound folder.\n"
            s += "You can do so by adding 'systemPath Some/Path' and 'soundPath some/Path' to your '{}' respectively.\n".format(CONFIG_FILE_VALUE)
        else:
            s += "Make sure '{}' and '{}' are both valid folders and '{}' contains all system sounds.\n".format(config(SOUND_PATH), config(RESOURCE_PATH), config(RESOURCE_PATH))

        raise RuntimeError(s)

def config(configName):
    if configName in CONFIG:
        if configName == SOUND_PATH or configName == RESOURCE_PATH:
            # Can never have too many slashes in paths
            return CONFIG[configName] + "/"
        return CONFIG[configName]

    if configName == HOTBAR_KEYS:
        return HOTBAR_KEYS_VALUE
    if configName == MODIFY_KEY:
        return MODIFY_KEY_VALUE

    if configName == CONFIG_FILE:
        return CONFIG_FILE_VALUE
    if configName == ERROR_FILE:
        return ERROR_FILE_VALUE

def processSounds():
    global SYSTEM_SOUNDS
    global SOUNDS_BY_STROKES

    # Add System sounds
    SYSTEM_SOUNDS = {
        RELOAD_SOUND : Sound(audioData = sf.read(config(RESOURCE_PATH) + config(RELOAD_SOUND))[0]),
        ENABLE_SOUND : Sound(audioData = sf.read(config(RESOURCE_PATH) + config(ENABLE_SOUND))[0]),
        DISABLE_SOUND : Sound(audioData = sf.read(config(RESOURCE_PATH) + config(DISABLE_SOUND))[0]),
        SHUTDOWN_SOUND : Sound(audioData = sf.read(config(RESOURCE_PATH) + config(SHUTDOWN_SOUND))[0]),
        READY_SOUND : Sound(audioData = sf.read(config(RESOURCE_PATH) + config(READY_SOUND))[0])
    }

    # Init arrays and fill with files from folder
    SOUNDS_BY_STROKES = [[Sound() for y in range(len(HOTBAR_KEYS_VALUE))] for x in range(len(HOTBAR_KEYS_VALUE))]
    for f in os.listdir(config(SOUND_PATH)):
        if re.match("[1-9]{2} .*\.wav", f):
            firstStroke = int(f[0]) - 1
            secondStroke = int(f[1]) - 1
            s = resolveSoundByStrokes(firstStroke, secondStroke)

            data, samplerate = sf.read(config(SOUND_PATH) + f)
            # Convert Mono to Stereo
            if data.ndim == 1:
                data = np.vstack((data, data)).T
            trimmedName = f[3:-4]

            s.audioData = data
            s.label = trimmedName

        if re.match("[1-9]{2}.*\.(jpg|png)", f):
            firstStroke = int(f[0]) - 1
            secondStroke = int(f[1]) - 1
            s = resolveSoundByStrokes(firstStroke, secondStroke)

            scaledImage = Image.open(config(SOUND_PATH) + f, mode="r").resize(
                (config(SOUND_IMAGE_EDGE_LENGTH), config(SOUND_IMAGE_EDGE_LENGTH)), Image.BICUBIC)
            s.image = scaledImage

def resolveSoundByName(soundID):
    if soundID is not None:
        return SYSTEM_SOUNDS[soundID]

    return None

def resolveSoundByStrokes(firstStroke, secondStroke):
    return SOUNDS_BY_STROKES[firstStroke][secondStroke]

def closeLogger():
    LOGGER.handlers[0].close()
    LOGGER.removeHandler(LOGGER.handlers[0])

def openLogger():
    handler = logging.FileHandler(ERROR_FILE_VALUE)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)

def handleError(string):
    openLogger()
    string += "\nYour available devices are listed below.\n"
    string += str(getDeviceInfo()) + "\n"
    LOGGER.error(string)
    closeLogger()