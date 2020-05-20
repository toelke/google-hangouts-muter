![demo](video/demo.gif)

# Hardware button for muting/unmuting google hangouts meet

One python-script that finds the first chrome-windows, screenshots the area where the "muted" icon is shown to see if hangouts is muted or not.

This only works if there is only one chrome window and it is on top.

Muting workes even when the windows is not on top, but still only when there is one. Sends ^D, which mutes hangouts.

## Protocol

### Computer -> Arduino

m: Turn on red light
u: Turn off red light
?: Blink red light

### Arduino -> Computer

1: The button was pressed
0: The button was not pressed
