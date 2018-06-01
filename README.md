Netlfix stops to ask whether you're still watching every so often. Unfortunately, my keyboard and mouse are not within reach when sitting on the sofa. So whenever Netflix stops, I have to get up and click a button.

Obviously, this is highly inconvenient, and I got annoyed enough to hack together this awful piece of script that can emulate a mouse click precisely on the 'continue' button. A click is emulated when the microphone picks up a sound that is louder than the ambient noise level.

Result: If Netflix stops, you simply shout at your computer, and it will continue. Progress!


USAGE
=====

1. Set the right value as `DISPSIZE` (it should match your screen resolution)
2. Run `HEY_LISTEN.py`
3. Shout whenever Netflix stops