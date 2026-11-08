# NetProwler V2

This is a Python project I made while learning Python.

## What it does

NetProwler is a clean, modern desktop WiFi monitor for Windows. It reads your adapter's live status straight from the `netsh` command and displays it in an easy-to-read dashboard — network name, connection state, signal strength, band, channel, security, and link speeds. One click refreshes everything.

## Features

- Shows the connected network name (SSID) and connection state
- Displays signal strength, band (2.4/5 GHz), and channel
- Shows radio type, authentication method, and cipher
- Shows receive and transmit speeds in Mbps
- One-click hard refresh button
- Clean dark-mode card layout built with CustomTkinter
- Auto refresh and colour coded symbols for easier understanding

## What I learned

- How to run a system command from Python with `subprocess.run()` and capture its output
- How to parse text line-by-line using `.startswith()` and `.split(":", 1)` to pull out just the value
- How to update many labels at once with `label.configure(text=...)`
- How to lay out a dashboard with `grid`, `weight`, and `uniform` so cards stretch evenly

## How to run

1. Install Python 3.8 or newer.
2. Install CustomTkinter:
   ```bash
   pip install customtkinter
   ```
3. Run the file:
   ```bash
   python wifiscope.py
   ```
4. **Note:** this app uses Windows' `netsh` command, so it only works on Windows. On non-English Windows, some field names differ — see the note in the code if labels show "—".

**Made with:** Python

## Improvements from V1

- Colour coded signals
- Disconnect button
- Connect button that recieves your input and tries to connect to the given wifi
- Auto refresh every 3 seconds
- Manual refresh button if a timeout error occurs

## Future improvements

- Add a signal strength progress bar
- Maybe Graphs


