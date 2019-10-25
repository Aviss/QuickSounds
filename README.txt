QUICKSOUNDS - SOUNDBOARD BY AVISS

	QuickSounds is a program that can play sounds simultaneously to up to two Sounddevices of your choosing.

	Combining this with "VB-Audio Virtual Cable" you can set up your system in a way that allows you to play sounds on an input device like your microphone.
	You can download "VB-Audio Virtual Cable" from here: https://www.vb-audio.com/Cable/

SETTING UP VB-AUDIO VIRTUAL CABLE

	After installing, go to your recording devices and make "Cable Output" your standard recording device
	Open the properties of your physical recording device and on the card "Listen" check "Listen to this device" and select "CABLE Input" from the dropdown menu.

	This will make the Virtual Cable act like your real input device.

SETTING UP QUICKSOUNDS

	Open the 'cfg.ini' file in this folder and check that there are the following values:

		microphone
		headphones
		systemPath
		soundPath

	Go ahead and enter the path to the folder where all of your sounds are stored after 'soundPath'.
	You should not need to modify 'systemPath' unless you want to store the system sounds and your overlay image in a separate location.
	If you haven't used the program yet it's best to leave 'microphone' at its default value and 'headphones' at '-1'

	Right now your 'cfg.ini' should look something like this:

		microphone CABLE INPUT MME
		headphones -1
		systemPath system
		soundPath A:/Path/To/Your/Sound/Files/

	Now just double-click the 'QuickSounds.exe' it should exit immediately and produce an 'error.log'
	In there you'll find a hint that your 'headphones' and 'microphone' settings are wrong. You'll also find a list of audio devices that are installed on your system

	Your 'headphone' setting should be set to the name of the entry that has the '<' at the start. That is your standard playback device.
	It is enough to choose a couple words that are uniquely identifying that line. 
	For example if your line looks like this:
		<  7 Speakers (2- High Definition Au, MME (0 in, 2 out)

	Putting 'Speakers MME' as the value for 'headphones' should be enough to get the program to recognize it.

	Start the 'QuickSounds.exe' again. If you did it right you should hear the start-up sound. If not check the error log. The errors should be self-explanatory
	That's it. Your Setup is complete.

SUPPORTED FORMAT

	As of now only 44100hz .wav audio files work correctly with the program.
	Non-wav files will be ignored, Files with different bitrates will sound either sped up or slowed down.

BINDING SOUNDS TO HOTKEYS

	Binding sounds is really simple.
	All you need to do is add the two number keys you want to bind the sound to before the file name. 
	Valid numbers are 1-9. 

	Here is an example:

		'crickets.wav' -> '37 crickets.wav'
		Pressing 'Alt gr' + '3' and then 'Alt gr' + '7' will play this sound.

KEY BINDINGS

	'Num Lock' 					: Cancel Playback		(Stop any sounds that are playing)
	'Num Lock' (Hold) 			: Shut Down				(Stop Program altogether)
	'Alt Gr' + '-' 				: Toggle Enabled		(Toggle if 'Play Sounds' is active)
	'Scroll Lock' (Hold) 		: Reload 				(Reprocess 'cfg.ini', system folder and sound folder)

	'Alt Gr' + 'Num Block 1-9' 	: Play Sounds			(First press opens the overlay listing the possible sounds with the second press)

CUSTOMIZABILITY

	Obviously the playback devices can be changed.
	But also the system sounds:
		
		'disable.wav'	(Plays when program is toggled to be disabled)
		'enable.wav'	(Plays when program is toggled to be enabled)
		'ready.wav'		(Plays after program start and reload)
		'reload.wav'	(Plays when program starts a reload)
		'shutdown.wav'	(Plays as the last sound before the program shuts down completely)
	
		(All system sounds are only played on your playback device NOT on your recording device)
		
	And the overlay:
		
		'overlay.png'	(Overlay showing possible sounds after first keypress)
		(Due to technical limitations half transparent pixels will be blended with black. Also white as a text color is not customizable yet)
		
	can be switched at will.
	