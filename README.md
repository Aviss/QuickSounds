# QuickSounds - A Soundboard by Aviss

QuickSounds is a small application that can play sounds simultaneously on two sound devices of your choosing.

Combining this with [VB-Audio Virtual Cable](https://www.vb-audio.com/Cable) you can set up your system in a way that allows you to layer sounds on top of whatever your microphone is recording.

## Setup

### Setting up VB-Audio Virtual Cable

After installing, go to your recording devices and make "Cable Output" your standard recording device.
Open the properties of your physical recording device and on the card "Listen", check "Listen to this device" and select "CABLE Input" from the device selection.

This will make the Virtual Cable act like your real input device, albeit with a couple of milliseconds of delay.

### Setting up QuickSounds

Open the `cfg.ini` file in this folder and look for the following line:

    soundPath A:/Path/To/Your/Sounds

Go ahead and enter the Folder where you want QuickSounds to pull sound files from. There don't have to be any files in it for now, but the folder itself should exist.

Start the `QuickSounds.exe`. If everything worked you should hear a start-up sound. If not, check the error log. The errors should be self-explanatory.
\
That's it. Your Setup is complete.

## Controls

The hotkey structure is fairly rigid, but should allow for easy control. 

All actions, save for shutting down the application or reloading require pressing a "Modify Key" to avoid triggering actions accidentally.

QuickSounds supports up to 81 sounds to be loaded at one time, divided into categories of 9. 
To play a sound, while holding the "Modify Key" first press the number of the category
then the number of the sound from that category that should be played on the Numpad.

### Key Bindings

| Key                     | Action           | Notes                                                   |
|-------------------------|------------------|---------------------------------------------------------|
| `Num Lock`              | Cancel Playback  | Stop any sounds that are playing                        |
| `Num Lock` (Hold)       | Shut Down        | Stop Program altogether                                 |
| `Alt Gr` + `-`          | Toggle Enabled   | Toggle if "Play Sounds" is active)                      |
| `Scroll Lock` (Hold)    | Reload           | Reprocess `cfg.ini`, resources and sound folder         |
| `Alt Gr` + `Numpad 1-9` | Play Sounds      | First press opens the category second press plays sound |

## Sounds

### Supported Formats

As of now, only 44100hz .wav audio files work correctly with the program.
Non-wav files will be ignored, files with different bitrates will sound either sped up or slowed down.

### Binding Sounds to Hotkeys

Binding sounds is really simple.
All you need to do is add a sound file to your sounds folder starting with its category number and sound number (Both of which you can choose freely). 
Valid numbers are 1-9. 

Here is an example:

`37 crickets.wav`: Pressing `Alt gr + 3` and then `Alt gr + 7` will play this sound.
    
### Customizability

In the `cfg.ini` more options than just the sounds folder are available. For example, system sounds and the overlay can be changed.

### Changing the Playback Device

If you want to configure a static playback device on which the sounds should be played back to you, you can change the `privateDevice` in the `cfg.ini`. 
Otherwise your default playback device is picked. 

First, remove the `#` at the start of the line containing `privateDevice`. 

Now just double-click the `QuickSounds.exe`. It should exit immediately and produce an `error.log`
In there you'll find a list of audio devices that are installed on your system

You can set your device to any entry containing `(0 in, 2 out)`. The entry with `<` at the start marks your standard playback device.
It is enough to choose a couple words that (in order) uniquely identify an entry. 
For example if you want to choose a device with an entry like this:

    <  7 Speakers (2- High Definition Au, MME (0 in, 2 out)

Your config could look like this:

    privateDevice Speakers High MME

    