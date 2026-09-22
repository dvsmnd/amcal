# AMCAL
# LED Strip Amperage Calculator

A small desktop tool for calculating the current (amps) and power (watts) draw of an LED strip, so you can pick the right power supply before you wire anything up.

Enter your supply voltage, LEDs per meter, and strip length, and it calculates total current draw, total power, and a recommended PSU rating with safety headroom included.

## Features

- Calculates total number of LEDs, total current draw, and total power consumption
- Built-in presets for common LED types (WS2812B, SK6812, 5050 SMD, 3528 SMD, 2835 SMD, 5mm through-hole) with typical current-per-LED values
- Manual override for current-per-LED if your strip's datasheet gives a different figure
- Recommends a PSU rating with a 20% safety margin, so your power supply isn't run at its max continuously

## Download

| Platform | File |
|---|---|
| macOS | `led-strip-calculator` (executable, no Python install required) |
| Any OS with Python | `led_strip_calculator.py` |

## Usage

### macOS executable

1. Download `led-strip-calculator` from this repo
2. Make it executable if needed: `chmod +x led-strip-calculator`
3. Double-click to run, or launch from Terminal: `./led-strip-calculator`

> **Note:** macOS may block the app the first time since it isn't signed with an Apple developer certificate. If you see a warning, go to **System Settings → Privacy & Security** and click **Open Anyway**.

### Python script

Requires Python 3 with Tkinter (included in most standard Python installs).

```bash
python led_strip_calculator.py
```

## How it works

```
Total LEDs      = LEDs per meter × strip length (m)
Total current   = (Total LEDs × current per LED (mA)) / 1000
Total power     = Supply voltage × total current
Recommended PSU = Total current × 1.2 (20% headroom)
```

## Notes

- Current-per-LED values vary by strip and by how many color channels are lit at once — always check your strip's datasheet for the most accurate figure.
- This tool calculates the *load* the strip places on a power supply; it doesn't account for voltage drop over long cable/strip runs, which may require injecting power at multiple points on longer strips.

## License

MIT
