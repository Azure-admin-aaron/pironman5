# Pironman 5

Pironman 5 case

Quick Links:

- [Pironman 5](#pironman-5)
  - [About Pironman5](#about-pironman5)
  - [Links](#links)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Update](#update)
  - [Compatible Systems](#compatible-systems)
    - [Ubuntu 24.04 server eth0 and wifi not work](#ubuntu-2404-server-eth0-and-wifi-not-work)
    - [Debug](#debug)
  - [About SunFounder](#about-sunfounder)
  - [Contact us](#contact-us)

## About Pironman5

## Links

- SunFounder Online Store &emsp; <https://www.sunfounder.com/>
- Documentation &emsp; <https://docs.sunfounder.com/en/latest/>

## Installation

For systems that don't have git, python3 pre-installed you need to install them first

```bash
sudo apt-get update
sudo apt-get install git python3 -y
```

Execute the installation script

```bash
cd ~
git clone https://github.com/sunfounder/pironman5.git
cd ~/pironman5
sudo python3 install.py
```

## Usage

### CLI Options

The `pironman5` command provides various configuration options:

```bash
# Show help
pironman5 --help

# Show current configuration
pironman5 --config
```

### OLED Display Options

Configure the OLED display:

```bash
# Enable/disable OLED display
pironman5 -oe true   # Enable
pironman5 -oe false  # Disable

# Set OLED rotation (0°, 90°, 180°, or 270°)
pironman5 -or 0      # Normal orientation (landscape 128x64)
pironman5 -or 90     # Rotate 90° clockwise (portrait 64x128)
pironman5 -or 180    # Rotate 180° (upside down, landscape 128x64)
pironman5 -or 270    # Rotate 270° clockwise (portrait 64x128)

# Show current OLED rotation
pironman5 -or

# Set which disk to display
pironman5 -od total  # Show total disk usage
pironman5 -od nvme   # Show specific disk

# Set which network interface IP to display
pironman5 -oi all    # Cycle through all IPs
pironman5 -oi eth0   # Show specific interface

# Set OLED sleep timeout (seconds, 0 to disable)
pironman5 -os 10
```

#### OLED Rotation Modes

The OLED display supports four rotation modes:

| Rotation | Mode | Canvas Size | Description |
|----------|------|-------------|-------------|
| 0° | Landscape | 128×64 | Default orientation |
| 90° | Portrait | 64×128 | Rotated 90° clockwise |
| 180° | Landscape | 128×64 | Upside down |
| 270° | Portrait | 64×128 | Rotated 270° clockwise |

**Portrait Mode (90° and 270°):** When using portrait mode, the display canvas is 64×128 pixels (narrow and tall). The `pironman5.oled_portrait` module handles the canvas creation and image rotation automatically. Content is drawn on the portrait canvas and then rotated before being sent to the hardware.

### RGB LED Options

```bash
# Set RGB color (hex format without #)
pironman5 -rc ff0000  # Red

# Set RGB brightness (0-100)
pironman5 -rb 50

# Set RGB style
pironman5 -rs breathing

# Set RGB speed (0-100)
pironman5 -rp 50

# Enable/disable RGB
pironman5 -re true
```

### Temperature Options

```bash
# Set temperature unit (C or F)
pironman5 -u C  # Celsius
pironman5 -u F  # Fahrenheit
```

### Service Commands

```bash
# Start the service in foreground
pironman5 start

# Stop the service
pironman5 stop

# Restart the service (use systemctl)
sudo systemctl restart pironman5.service
```

## Update

<https://github.com/sunfounder/pironman5/blob/main/CHANGELOG.md>

## Compatible Systems

Operate Systems that passed the test on the Raspberry Pi 5:

Operate System | Release Date | Compatible
:---   | :---: | :---: 
Raspberry Pi OS Desktop - Trixie (64 bit) | 2025-10-01 | &#x2705;
Raspberry Pi OS Desktop - Trixie (32 bit) | 2025-10-01 |  &#x2705;
Raspberry Pi OS Full - Trixie (64 bit) | 2025-10-01 |  &#x2705;
Raspberry Pi OS Full - Trixie (32 bit) | 2025-10-01 |  &#x2705;
Raspberry Pi OS lite - Trixie (64 bit) | 2025-10-01 |  &#x2705;
Raspberry Pi OS lite - Trixie (64 bit) | 2025-10-01 |  &#x2705;
Ubuntu Desktop 25.04 LTS (64 bit) | 2025-04-17 |  &#x2705;
Ubuntu Server 25.04 LTS (64 bit) | 2025-04-17 |  &#x2705;
Ubuntu Desktop 25.10 (64 bit) | 2025-10-09 |   &#x2705;
Ubuntu Server 25.10 (64 bit) | 2025-10-09 |   &#x2705;
Kali Linux | 2025-09-18 | &#x2705;
Home Assistant OS 16.3 | 2025-11-04 | &#x2705;
Homebridge bookworm (64 bit) | 2025-07-16 | &#x2705;
Homebridge bookworm (64 bit) | 2025-07-16 | &#x2705;
Umbrel OS 1.5 | 2025-11-5 | &#x2705;

### Debug

Clone the dependency you want to debug or edit

```bash
git clone https://github.com/sunfounder/pironman5.git
git clone https://github.com/sunfounder/pm_dashboard.git
git clone https://github.com/sunfounder/pm_auto.git
git clone https://github.com/sunfounder/sf_rpi_status.git
```

Make adjustments, and manually install the package

```bash
cd ~/pironman5 && sudo /opt/pironman5/venv/bin/pip3 uninstall pironman5 -y && sudo /opt/pironman5/venv/bin/pip3 install . --no-build-isolation
cd ~/pm_dashboard && sudo /opt/pironman5/venv/bin/pip3 uninstall pm_dashboard -y && sudo /opt/pironman5/venv/bin/pip3 install . --no-build-isolation
cd ~/pm_auto && sudo /opt/pironman5/venv/bin/pip3 uninstall pm_auto -y && sudo /opt/pironman5/venv/bin/pip3 install . --no-build-isolation
cd ~/sf_rpi_status && sudo /opt/pironman5/venv/bin/pip3 uninstall sf_rpi_status -y && sudo /opt/pironman5/venv/bin/pip3 install . --no-build-isolation
```

Start/stop the service for debug

```
sudo systemctl stop pironman5.service
sudo systemctl start pironman5.service
sudo systemctl restart pironman5.service
sudo pironman5 start

sudo /opt/pironman5/venv/bin/python3
```

## About SunFounder

SunFounder is a company focused on STEAM education with products like open source robots, development boards, STEAM kit, modules, tools and other smart devices distributed globally. In SunFounder, we strive to help elementary and middle school students as well as hobbyists, through STEAM education, strengthen their hands-on practices and problem-solving abilities. In this way, we hope to disseminate knowledge and provide skill training in a full-of-joy way, thus fostering your interest in programming and making, and exposing you to a fascinating world of science and engineering. To embrace the future of artificial intelligence, it is urgent and meaningful to learn abundant STEAM knowledge.

## Contact us

website:
    www.sunfounder.com

E-mail:
    service@sunfounder.com
