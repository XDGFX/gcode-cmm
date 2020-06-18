# gcode-cmm
### Adapt a USB-controllable 3D printer into a CMM machine
*Tested with an Ender 3 2020, but should work with any printer that accepts GCODE commands over USB serial.*

## Intro
I wrote this quickly because I broke one of the mirror caps on my Subaru WRX. As I couldn't buy the caps on their own, instead needing to get a whole new mirror off eBay for £30, I decided to do the next logical thing and buy a 3D printer to make my own.

This software allows you to control a 3D printer head with keyboard controls, and save position data points to a file, effectively functioning as a CMM (coordinate measuring machine). Everything is manual, but this also means no additional hardware is required.

## Installation
Simply clone and run! You may need to install `pyserial`. Tested to work on macOS and WSL, untested on Windows.
```bash
git clone https://github.com/XDGFX/gcode-cmm.git
sudo chmod +x gcode-cmm/cmm.py
python3 cmm.py
```
```bash
# Installing pyserial if required
pip3 install pyserial==3.4
```

Open `settings.json` and edit as required. the `points_n` and `dist_n` are only used in the *rectangle* mode.

## Use
There are two modes available, *free* and *rectangle*. *Free* allows full control over the printer head, and saving of any number of points. *Rectangle* will create a rectangular grid of evenly spaced points, and you only control the Z axis. Currently I have only properly used the *free* mode so use *rectangle* at your own risk.

I needed to measure some heavy curvature, and so attached the included nozzle cleaner needle to the printer head. This worked well, as the needle would bend if touching the part; without moving the part or offsetting the head.

Start the software, select the mode you want, and the controls should be visible on the console.

## Required GCODE Support
The following table shows which GCODE commands need to be supported by the printer - it's pretty basic so I would be surprised if your printer doesn't work.
| Command | Description | Vital? |
|--|--|--|
| G0 | Movement | Yes |
| G28 | Automatic Homing | Yes |
| M107 P1 | Turn off part cooling fan | No |

## Examples

#### External Scan Points
![Gif of a rotating point cloud showing a scan of the outside of a mirror cap, with complex curvature.](https://media.giphy.com/media/M9BH4BEoEGnzIiF9GH/giphy.gif)

#### Internal Scan Points
![Gif of a rotating point cloud showing the inside features of a mirror cap, including intricate details and features.](https://media.giphy.com/media/mAIFahzhuBKQQfCEjL/giphy.gif)

#### Completed CAD Model
![Gif of the completed CAD model using the two previous datapoint sets, which can then be sliced and printed.](https://media.giphy.com/media/LMci9hWpo51xEHtoMR/giphy.gif)

#### Original Part
![Picture of the inside of a factory Subaru mirror cap](https://i.imgur.com/fzwelO3.jpg)