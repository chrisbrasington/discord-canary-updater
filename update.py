#!/usr/bin/env python3
import os
import subprocess
import requests
import re

def get_installed_version():
    """Gets the currently installed version of Discord Canary."""
    try:
        result = subprocess.run([
            "dpkg-query", "-W", "-f='${Version}'", "discord-canary"
        ], capture_output=True, text=True, check=True)
        return result.stdout.strip().strip("'")
    except subprocess.CalledProcessError:
        return None

def get_latest_version():
    """Fetches the latest available version of Discord Canary from the website."""
    url = "https://discord.com/api/download/canary?platform=linux"
    try:
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        redirect_url = response.headers.get("Location")
        if redirect_url:
            match = re.search(r"discord-canary-(\d+\.\d+\.\d+)", redirect_url)
            if match:
                return match.group(1), redirect_url
        return None, None
    except requests.RequestException as e:
        print(f"Error fetching the latest version: {e}")
        return None, None

def download_and_install(download_url):
    """Downloads and installs the latest version of Discord Canary."""
    deb_file = "/tmp/discord-canary-latest.deb"
    try:
        print("Downloading the latest version...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open(deb_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print("Installing the latest version...")
        subprocess.run(["sudo", "dpkg", "-i", deb_file], check=True)
        print("Installation completed.")
    except requests.RequestException as e:
        print(f"Error downloading the update: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing the update: {e}")
    finally:
        if os.path.exists(deb_file):
            os.remove(deb_file)

def launch_discord():
    """Launches Discord Canary."""
    try:
        print("Launching Discord Canary...")
        subprocess.Popen(
            ["discord-canary", "--no-sandbox", "--disable-features=UseOzonePlatform"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("Discord Canary is not installed.")

def main():
    installed_version = get_installed_version()
    latest_version, download_url = get_latest_version()

    if latest_version is None:
        print("Unable to fetch the latest version.")
        return

    print(f"Installed version: {installed_version}")
    print(f"Latest version: {latest_version}")

    if installed_version != latest_version:
        print("Update available. Updating...")
        download_and_install(download_url)
    else:
        print("Discord Canary is already up to date.")

    launch_discord()

if __name__ == "__main__":
    main()
