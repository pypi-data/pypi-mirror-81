# metropy

Metronome with a minimal UI, written in Python 3 + ncurses.

Features:
- Change BPM
- Change Beats Per Bar
- Start/Stop metronome
- Customizable sounds (via --bar and --beat)
- BPM detector

### Install

```sh
pip install metropy
```

### Usage

```
usage: metropy [-h] [--bar BAR_SOUND] [--beat BEAT_SOUND] [bpm] [beats]

Metronome with Terminal UI in ncurses.

positional arguments:
  bpm                BPM (default is 60)
  beats              Beats per bar (default is 4)

optional arguments:
  -h, --help         show this help message and exit
  --bar BAR_SOUND    Path of the bar sound (.wav)
  --beat BEAT_SOUND  Path of the beat sound (.wav)

```

### Example

```sh
metropy
```


```sh
metropy --bar /path/to/bar/sound.wav --beat /path/to/beat/sound.wav
```

Sometimes ALSA reports problem but the metronome will work anyway.  
As always, you can suppress the errors with:
```
metropy 2> /dev/null
```

### What it looks like

![metropy-help](img/metropy-help.png) 


![metropy-playing](img/metropy-playing.png) 


![metropy-detector](img/metropy-detector.png) 