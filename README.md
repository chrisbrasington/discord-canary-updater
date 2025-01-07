# Discord Canary Updater

This script checks for the latest version of Discord Canary available for download in `.deb` format, compares it to the version currently installed on your Debian-based system, and updates it if necessary.

## Usage
   ```bash
   python3 update.py
   ```

## Features
- Detects the currently installed version of Discord Canary.
- Fetches the latest available `.deb` version from Discord's servers.
- Automatically downloads and installs updates using `dpkg`.
- Launches Discord Canary after updating.
    - (may not launch from vscode terminal for some reason)

## Requirements
- Python 3.6 or later
- `requests` library (`pip install requests`)
- Debian-based operating system (e.g., Ubuntu)


## Notes
- Ensure you have `sudo` privileges to install `.deb` packages. (may not be required)
- This script is designed for `.deb` packages only and will not work for other package formats.

## Troubleshooting
- If Discord Canary fails to launch after updating, try running it with the following command:
  ```bash
  discord-canary --no-sandbox --disable-features=UseOzonePlatform
  ```