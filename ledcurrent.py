#!/usr/bin/env python3
"""
LED Strip Amperage Calculator
------------------------------
A simple GUI tool to calculate the current (amps) and power (watts) draw
of an LED strip based on supply voltage, LEDs per meter, strip length,
and current draw per individual LED.

Run with:  python led_strip_calculator.py
Requires only the standard library (tkinter).
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Common LED types and their typical current draw per LED (in mA).
# These are rough, widely-used reference values - always check your
# specific LED strip's datasheet for accurate numbers.
LED_PRESETS = {
    "Custom (enter manually)": None,
    "WS2812B / NeoPixel (addressable RGB)": 60.0,
    "SK6812 (addressable RGBW)": 80.0,
    "5050 SMD (single color)": 20.0,
    "5050 SMD (RGB, all channels on)": 60.0,
    "3528 SMD (single color)": 20.0,
    "2835 SMD (single color)": 20.0,
    "5mm through-hole LED": 20.0,
}

SAFETY_MARGIN = 0.20  # recommend sizing the PSU 20% above calculated draw


class LedStripCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LED Strip Amperage Calculator")
        self.resizable(False, False)
        self.configure(padx=16, pady=16)

        self._build_widgets()

    def _build_widgets(self):
        row = 0

        ttk.Label(self, text="LED Strip Amperage Calculator", font=("Segoe UI", 13, "bold")).grid(
            row=row, column=0, columnspan=2, pady=(0, 12), sticky="w"
        )
        row += 1

        # Supply voltage
        ttk.Label(self, text="Supply voltage (V):").grid(row=row, column=0, sticky="w", pady=4)
        self.voltage_var = tk.StringVar(value="12")
        ttk.Entry(self, textvariable=self.voltage_var, width=15).grid(row=row, column=1, pady=4)
        row += 1

        # LEDs per meter
        ttk.Label(self, text="LEDs per meter:").grid(row=row, column=0, sticky="w", pady=4)
        self.leds_per_m_var = tk.StringVar(value="60")
        ttk.Entry(self, textvariable=self.leds_per_m_var, width=15).grid(row=row, column=1, pady=4)
        row += 1

        # Strip length
        ttk.Label(self, text="Strip length (m):").grid(row=row, column=0, sticky="w", pady=4)
        self.length_var = tk.StringVar(value="5")
        ttk.Entry(self, textvariable=self.length_var, width=15).grid(row=row, column=1, pady=4)
        row += 1

        # LED type preset dropdown
        ttk.Label(self, text="LED type preset:").grid(row=row, column=0, sticky="w", pady=4)
        self.preset_var = tk.StringVar(value=list(LED_PRESETS.keys())[0])
        preset_menu = ttk.Combobox(
            self, textvariable=self.preset_var, values=list(LED_PRESETS.keys()),
            state="readonly", width=32
        )
        preset_menu.grid(row=row, column=1, pady=4, sticky="w")
        preset_menu.bind("<<ComboboxSelected>>", self._on_preset_selected)
        row += 1

        # Current per LED (manual / overridable)
        ttk.Label(self, text="Current per LED (mA):").grid(row=row, column=0, sticky="w", pady=4)
        self.ma_per_led_var = tk.StringVar(value="20")
        ttk.Entry(self, textvariable=self.ma_per_led_var, width=15).grid(row=row, column=1, pady=4)
        row += 1

        ttk.Separator(self, orient="horizontal").grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1

        # Calculate button
        ttk.Button(self, text="Calculate", command=self.calculate).grid(
            row=row, column=0, columnspan=2, pady=(0, 10)
        )
        row += 1

        # Results
        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1

        self.result_vars = {
            "total_leds": tk.StringVar(value="-"),
            "total_current": tk.StringVar(value="-"),
            "total_power": tk.StringVar(value="-"),
            "recommended_psu": tk.StringVar(value="-"),
        }

        labels = [
            ("Total LEDs:", "total_leds"),
            ("Total current draw:", "total_current"),
            ("Total power draw:", "total_power"),
            (f"Recommended PSU rating (+{int(SAFETY_MARGIN*100)}% headroom):", "recommended_psu"),
        ]

        for i, (label_text, key) in enumerate(labels):
            ttk.Label(self.result_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=2)
            ttk.Label(self.result_frame, textvariable=self.result_vars[key], font=("Segoe UI", 10, "bold")).grid(
                row=i, column=1, sticky="w", padx=(8, 0), pady=2
            )

    def _on_preset_selected(self, event=None):
        preset = self.preset_var.get()
        ma = LED_PRESETS.get(preset)
        if ma is not None:
            self.ma_per_led_var.set(str(ma))

    def calculate(self):
        try:
            voltage = float(self.voltage_var.get())
            leds_per_m = float(self.leds_per_m_var.get())
            length = float(self.length_var.get())
            ma_per_led = float(self.ma_per_led_var.get())

            if voltage <= 0 or leds_per_m <= 0 or length <= 0 or ma_per_led <= 0:
                raise ValueError("All values must be greater than zero.")
        except ValueError as e:
            messagebox.showerror(
                "Invalid input",
                "Please enter valid positive numbers in all fields.\n\n" + str(e)
                if str(e) else "Please enter valid positive numbers in all fields."
            )
            return

        total_leds = leds_per_m * length
        total_current_a = (total_leds * ma_per_led) / 1000.0
        total_power_w = voltage * total_current_a
        recommended_a = total_current_a * (1 + SAFETY_MARGIN)

        self.result_vars["total_leds"].set(f"{total_leds:.0f} LEDs")
        self.result_vars["total_current"].set(f"{total_current_a:.2f} A")
        self.result_vars["total_power"].set(f"{total_power_w:.1f} W")
        self.result_vars["recommended_psu"].set(f"{recommended_a:.2f} A  (at {voltage:.0f} V)")


if __name__ == "__main__":
    app = LedStripCalculator()
    app.mainloop()