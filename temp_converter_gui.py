# finished on: 21-09-2025

import tkinter as tk
from tkinter import ttk, messagebox
import re # might need this for validation later?

# ---------- Conversion helper functions ----------
def c_to_f(c): return (c * 9/5) + 32
def c_to_k(c): return c + 273.15
def f_to_c(f): return (f - 32) * 5/9
def f_to_k(f): return (f - 32) * 5/9 + 273.15
def k_to_c(k): return k - 273.15
def k_to_f(k): return (k - 273.15) * 9/5 + 32

# this is the main app class
class TempConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Temperature Converter")
        self.geometry("480x320") # hardcoded size
        self.resizable(False, False)

        # IMPORTANT FLAG!! this stops the slider and entry box from fighting each other
        # got stuck on this for a while lol
        self.is_updating_ui = False

        # App variables
        self.entry_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.result_var.set("Enter a value to get started.")

        self._setup_style()
        self.create_widgets() # changed name to be more clear
        self._bind_events()

    def _setup_style(self):
        # this is where the colors and stuff go
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.configure(background="#1F2937")
        self.style.configure("TFrame", background="#111827")
        self.style.configure("TLabel", background="#111827", foreground="#F7FBFF", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Result.TLabel", font=("Segoe UI", 12), foreground="#3B82F6")
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="#1F2937", foreground="#F7FBFF", insertcolor="#F7FBFF")
        self.style.configure("Horizontal.TScale", background="#111827")

    def create_widgets(self):
        # create the main frame that holds everything
        MainFrame = ttk.Frame(self, padding=20)
        MainFrame.pack(expand=True, fill="both", padx=10, pady=10)
        MainFrame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(MainFrame, text="🌡️ Temperature Converter", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Frame for the inputs
        input_frame = ttk.Frame(MainFrame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        # Entry box for typing the temperature
        ttk.Label(input_frame, text="Enter Temperature").grid(row=0, column=0, sticky="w")
        temp_entry_box = ttk.Entry(input_frame, textvariable=self.entry_var, width=20)
        temp_entry_box.grid(row=1, column=0, sticky="ew", ipady=4)
        temp_entry_box.focus()

        # Dropdown for the scale
        ttk.Label(input_frame, text="From Scale").grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.scale_combo = ttk.Combobox(
            input_frame,
            values=["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
            state="readonly",
            width=15
        )
        self.scale_combo.grid(row=1, column=1, sticky="ew", padx=(10, 0), ipady=2)
        self.scale_combo.current(0) # Default to Celsius

        # a slider for fun
        self.slider = ttk.Scale(MainFrame, from_=-100, to=200, orient="horizontal")
        self.slider.grid(row=2, column=0, columnspan=2, sticky="ew", pady=20)

        # where the result is shown
        ttk.Label(MainFrame, text="Result:", font=("Segoe UI", 11, "bold")).grid(row=3, column=0, sticky="w")
        result_label = ttk.Label(MainFrame, textvariable=self.result_var, style="Result.TLabel")
        result_label.grid(row=3, column=1, sticky="w", padx=10)

        # the buttons at the bottom
        button_frame = ttk.Frame(MainFrame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="sew", pady=(20, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        copyButton = ttk.Button(button_frame, text="Copy Result", command=self._copy_result)
        copyButton.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        clearButton = ttk.Button(button_frame, text="Clear", command=self._clear_inputs)
        clearButton.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _bind_events(self):
        # make things happen when user does stuff
        self.entry_var.trace_add("write", self._on_entry_change)
        self.slider.config(command=self._on_slider_move)
        self.scale_combo.bind("<<ComboboxSelected>>", self._on_entry_change)
        self.bind("<Return>", lambda e: self._copy_result())

    def _on_slider_move(self, value_str):
        # called when the slider is moved by the user
        if self.is_updating_ui: return
        print(f"DEBUG: Slider value is {value_str}") # for debugging
        self.is_updating_ui = True
        self.entry_var.set(f"{float(value_str):.1f}")
        self._perform_conversion()
        self.is_updating_ui = False

    def _on_entry_change(self, *args):
        # called when the text in the entry box changes
        if self.is_updating_ui: return
        print("DEBUG: Entry text changed") # for debugging
        self.is_updating_ui = True
        value = self._get_input_value()
        if isinstance(value, float):
            # make sure value is in slider range to prevent crash
            if value > 200: value = 200
            if value < -100: value = -100
            self.slider.set(value)
            self._perform_conversion()
        self.is_updating_ui = False

    def _get_input_value(self):
        # function to safely get the number from the entry box
        raw = self.entry_var.get()
        try:
            return float(raw)
        except ValueError:
            if raw != "" and raw != "-": # allow typing a minus sign
                self.result_var.set("Invalid input: Not a number.")
            return None

    # a helper function to make the numbers look nice
    def format_number_nicely(self, num):
        return f"{num:.2f}".rstrip('0').rstrip('.')

    def _perform_conversion(self):
        # this is the main logic for the conversion
        value = self._get_input_value()
        if value is None:
            return

        scale = self.scale_combo.get()

        if "Celsius" in scale:
            f = c_to_f(value)
            k = c_to_k(value)
            res = f"{self.format_number_nicely(f)} °F  |  {self.format_number_nicely(k)} K"
            self.result_var.set(res)
        elif "Fahrenheit" in scale:
            c = f_to_c(value)
            k = f_to_k(value)
            res = f"{self.format_number_nicely(c)} °C  |  {self.format_number_nicely(k)} K"
            self.result_var.set(res)
        elif "Kelvin" in scale:
            c = k_to_c(value)
            f = k_to_f(value)
            res = f"{self.format_number_nicely(c)} °C  |  {self.format_number_nicely(f)} °F"
            self.result_var.set(res)


    def _clear_inputs(self):
        # this clears the text box
        self.is_updating_ui = True
        self.entry_var.set("")
        self.slider.set(0) # reset slider to 0
        self.result_var.set("Cleared. Enter a new value.")
        self.is_updating_ui = False

    def _copy_result(self):
        # for the copy button
        result = self.result_var.get()
        if "Enter a value" not in result and "Invalid" not in result:
            self.clipboard_clear()
            self.clipboard_append(result)
            messagebox.showinfo("Copied!", "Copied the result to your clipboard!")
        else:
            messagebox.showwarning("Oops!", "Nothing to copy yet.")

# this makes the app run
if __name__ == "__main__":
    app = TempConverterApp()
    app.mainloop()