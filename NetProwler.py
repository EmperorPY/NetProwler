# Import customtkinter for the modern-looking UI widgets
import customtkinter as ctk
# Import subprocess so we can run the netsh command
import subprocess

# Set the app to dark mode
ctk.set_appearance_mode("dark")

def disconnect():
    try:
        # Executes: netsh wlan disconnect
        result = subprocess.run(
            ["netsh", "wlan", "disconnect"], 
            capture_output=True, 
            text=True, 
            check=True
        )
    except subprocess.CalledProcessError:
        error_label.configure(text="Error disconnecting WiFi")

def auto_update():
    refresh()
    root.after(3000, auto_update)  # Update every 3 seconds

# This function runs the netsh command and updates every label on screen.
# It's called on startup and every time the user clicks "Refresh".
def refresh():
    # Run the Windows command that lists WiFi adapter info
    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    # Grab the raw text output from the command
    output = result.stdout

    # Go through each line of the output looking for the fields we want
    for line in output.splitlines():
        # Trim whitespace so startswith works cleanly
        line = line.strip()

        # SSID is the network name. We skip BSSID (that's the router MAC address)
        if line.startswith("SSID") and "BSSID" not in line:
            ssid_value.configure(text=line.split(":", 1)[1].strip())

        # Connection state ("connected" or "disconnected")
        elif line.startswith("State"):
            state_value.configure(text=line.split(":", 1)[1].strip())

        # Signal strength (e.g. "85%")
        elif line.startswith("Signal"):
            signal_value.configure(text=line.split(":", 1)[1].strip())

        # Frequency band (2.4 GHz or 5 GHz)
        elif line.startswith("Band"):
            band_value.configure(text=line.split(":", 1)[1].strip())

        # WiFi channel number
        elif line.startswith("Channel"):
            channel_value.configure(text=line.split(":", 1)[1].strip())

        # Radio type (802.11ac, 802.11ax, etc.)
        elif line.startswith("Radio type"):
            radio_value.configure(text=line.split(":", 1)[1].strip())

        # Security method (WPA2-Personal, WPA3, etc.)
        elif line.startswith("Authentication"):
            auth_value.configure(text=line.split(":", 1)[1].strip())

        # Encryption cipher (CCMP, TKIP, etc.)
        elif line.startswith("Cipher"):
            cipher_value.configure(text=line.split(":", 1)[1].strip())

        # Download speed in Mbps
        elif line.startswith("Receive rate"):
            rx_value.configure(text=line.split(":", 1)[1].strip())
            if float(line.split(":", 1)[1].strip().split(" ")[0]) <= 100:
                rx_value.configure(text_color="red")
            elif float(line.split(":", 1)[1].strip().split(" ")[0]) <= 299:
                rx_value.configure(text_color="orange")
            elif float(line.split(":", 1)[1].strip().split(" ")[0]) <= 999:
                rx_value.configure(text_color="green")
            elif float(line.split(":", 1)[1].strip().split(" ")[0]) >= 1000:
                rx_value.configure(text_color="cyan")


        # Upload speed in Mbps
        elif line.startswith("Transmit rate"):
            tx_value.configure(text=line.split(":", 1)[1].strip())
            if float(line.split(":", 1)[1].strip().split(" ")[0]) <= 100:
                tx_value.configure(text_color="red")
            elif float(line.split(":", 1)[1].strip().split(" ")[0]) <= 299:
                tx_value.configure(text_color="orange")
            elif float(line.split(":", 1)[1].strip().split(" ")[0]) <= 999:
                tx_value.configure(text_color="green")
            elif float(line.split(":", 1)[1].strip().split(" ")[0]) >= 1000:
                tx_value.configure(text_color="cyan")


# ---------------- BUILD THE WINDOW ----------------

root = ctk.CTk()
root.title("NetProwler")

# Full screen minus task bar
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
task_bar_height = 50
window_height = screen_height - task_bar_height
root.geometry(f"{screen_width}x{window_height}+0+0")

# Grid: let the cards area stretch
root.grid_rowconfigure(0, weight=0)   # title bar
root.grid_rowconfigure(1, weight=0)   # refresh bar
root.grid_rowconfigure(2, weight=1)   # cards area
root.grid_columnconfigure(0, weight=1)

# ---------------- TITLE BAR (its own frame) ----------------
title_frame = ctk.CTkFrame(root, corner_radius=20)
title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))

title_label = ctk.CTkLabel(
    title_frame,
    text="NETPROWLER",
    font=("Arial", 55, "bold"),
    text_color="white",
)
title_label.pack(pady=(15, 0))

subtitle_label = ctk.CTkLabel(
    title_frame,
    text="Live WiFi status straight from your adapter",
    font=("Arial", 16),
    text_color="lightgrey",
)
subtitle_label.pack(pady=(0, 15))

# ---------------- REFRESH BAR (its own frame) ----------------
refresh_frame = ctk.CTkFrame(root, corner_radius=20)
refresh_frame.grid(row=1, column=0, pady=5, padx=20, sticky="ew")


refresh_button = ctk.CTkButton(
    refresh_frame,
    text="Manual Refresh",
    command=refresh,
    font=("Arial", 16, "bold"),
    width=160,
    height=40,
    fg_color="darkgrey",
    hover_color="lightgrey",
    text_color="black",
    corner_radius=10,
)
refresh_button.pack(pady=5)

wifi_entry = ctk.CTkEntry(
    refresh_frame,
    placeholder_text="WiFi Name",
    font=("Arial", 16),
    width=300,
    height=40,
    fg_color="darkgrey",
    text_color="black",
    corner_radius=10,
)

wifi_entry.pack(pady=5)

interface_entry = ctk.CTkEntry(
    refresh_frame,
    placeholder_text="Interface",
    font=("Arial", 16),
    width=300,
    height=40,
    fg_color="darkgrey",
    text_color="black",
    corner_radius=10,
)

interface_entry.pack(pady=5)

def connect():
    
    try:
        wifi_name = wifi_entry.get()
        interface_name = interface_entry.get()
        # Executes: netsh wlan connect name=<wifi_name> interface=<interface_name>
        result = subprocess.run(
            ["netsh", "wlan", "connect", "name=" + wifi_name, "interface=" + interface_name], 
            capture_output=True, 
            text=True, 
            check=True
        )
    except subprocess.CalledProcessError as e:
        error_label.configure(text="Error connecting WiFi")

connect_button = ctk.CTkButton(
    refresh_frame,
    text="Connect",
    command=connect,
    font=("Arial", 16, "bold"),
    width=160,
    height=40,
    fg_color="darkgrey",
    hover_color="lightgrey",
    text_color="black",
    corner_radius=10,
)

connect_button.pack(pady=5)





disconnect_button = ctk.CTkButton(
    refresh_frame,
    text="Disconnect",
    command=disconnect,
    font=("Arial", 16, "bold"),
    width=160,
    height=40,
    fg_color="darkgrey",
    hover_color="lightgrey",
    text_color="black",
    corner_radius=10,
)
disconnect_button.pack()





error_label = ctk.CTkLabel(refresh_frame, text="", text_color="red")
error_label.pack(pady=(10, 0))
# ---------------- CARDS AREA (its own frame) ----------------
cards_frame = ctk.CTkFrame(root, fg_color="transparent")
cards_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

# 3 columns of equal width, 4 rows of equal height
for c in range(3):
    cards_frame.grid_columnconfigure(c, weight=1)
for r in range(4):
    cards_frame.grid_rowconfigure(r, weight=1)


# Helper function to build one "card" (a titled box showing one value)
def make_card(parent, title, emoji):
    card = ctk.CTkFrame(parent, corner_radius=95)
    header = ctk.CTkLabel(
        card, text=f"{emoji} {title}", font=("Arial", 16, "bold"),
        text_color="lightgrey",
    )
    header.pack(pady=(15, 5))
    value = ctk.CTkLabel(card, text="—", font=("Arial", 28, "bold"), text_color="white")
    value.pack(pady=(0, 15), expand=True)
    return card, value


# ---------- Network banner (spans all 3 columns) ----------
network_card = ctk.CTkFrame(cards_frame, corner_radius=20)
network_card.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

# Big bold network name at the top of the banner
ssid_value = ctk.CTkLabel(
    network_card, text="Searching…", font=("Arial", 26, "bold"),
    text_color="white",
)
ssid_value.pack(pady=(15, 5))

# Smaller connection state below it
state_value = ctk.CTkLabel(
    network_card, text="", font=("Arial", 18), text_color="lightgrey",
)
state_value.pack(pady=(0, 15))

# ---------- Row 1: Signal, Band, Channel ----------
signal_card, signal_value = make_card(cards_frame, "Signal", "📶")
signal_card.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

band_card, band_value = make_card(cards_frame, "Band", "📡")
band_card.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

channel_card, channel_value = make_card(cards_frame, "Channel", "🎯")
channel_card.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)

# ---------- Row 2: Radio type, Authentication, Cipher ----------
radio_card, radio_value = make_card(cards_frame, "Radio type", "📻")
radio_card.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

auth_card, auth_value = make_card(cards_frame, "Authentication", "🔒")
auth_card.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)

cipher_card, cipher_value = make_card(cards_frame, "Cipher", "🔑")
cipher_card.grid(row=2, column=2, sticky="nsew", padx=10, pady=5)

# ---------- Row 3: Receive rate, Transmit rate (span 3 columns in pairs) ----------
rx_card, rx_value = make_card(cards_frame, "Receive rate", "⬇️")
rx_card.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=10, pady=5)

tx_card, tx_value = make_card(cards_frame, "Transmit rate", "⬆️")
tx_card.grid(row=3, column=1, columnspan=2, sticky="nsew", padx=10, pady=5)

# Load the values once when the app opens

auto_update()
# Start the app's main event loop
root.mainloop()
