# finished on: 21-09-2025

# ---------- Conversion helper functions ----------
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# ---------- Console Interface ----------
print("🌡️ Temperature Converter 🌡️")
print("Select the input scale:")
print("1. Celsius")
print("2. Fahrenheit")
print("3. Kelvin")

choice = int(input("Enter choice (1/2/3): "))

temp = float(input("Enter the temperature value: "))

# Perform conversions based on user choice
if choice == 1:
    print(f"{temp} °C = {celsius_to_fahrenheit(temp):.2f} °F")
    print(f"{temp} °C = {celsius_to_kelvin(temp):.2f} K")
elif choice == 2:
    print(f"{temp} °F = {fahrenheit_to_celsius(temp):.2f} °C")
    print(f"{temp} °F = {fahrenheit_to_kelvin(temp):.2f} K")
elif choice == 3:
    print(f"{temp} K = {kelvin_to_celsius(temp):.2f} °C")
    print(f"{temp} K = {kelvin_to_fahrenheit(temp):.2f} °F")
else:
    print("Invalid choice!")