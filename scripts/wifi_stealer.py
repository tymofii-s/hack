import subprocess
import re


def get_wifi_passwords():
    # Get a list of all Wi-Fi profiles
    profiles_data = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
    profiles = re.findall(r"All User Profile\s*:\s(.*)", profiles_data.stdout)

    wifi_list = []

    for profile in profiles:
        # Get the password for each network
        profile = profile.strip()
        profile_data = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True)
        password_match = re.search(r"Key Content\s*:\s(.*)", profile_data.stdout)

        password = password_match.group(1) if password_match else "No password (or hidden)"
        wifi_list.append((profile, password))

    return wifi_list

def save_info(info: list):
    wifis = "\n".join(info)

    output = open("data/output.txt", mode="a", encoding="utf-8")
    output.write("Wi-Fi passwords:\n")
    output.write(wifis)

wifis = []
if __name__ == "__main__":
    wifi_data = get_wifi_passwords()
    for ssid, password in wifi_data:
        wifis.append(f"Wi-Fi: {ssid} | Password: {password}")

save_info(wifis)