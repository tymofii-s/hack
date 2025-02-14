import subprocess

def run_scripts_from_list(scripts):
    processes = []
    for script in scripts:
        print(f"Launching {script}...")
        try:
            process = subprocess.Popen(["python", script])
            processes.append(process)
        except Exception as e:
            print(f"Startup error {script}: {e}")
    
    # Waiting for the completion of all processes
    for process in processes:
        process.wait()

def run_scripts_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            scripts = [line.strip() for line in file if line.strip()]
        run_scripts_from_list(scripts)
    except FileNotFoundError:
        print(f"File {filename} not found.")

if __name__ == "__main__":
    # Option 1: list of scripts in code
    scripts = ["script1.py", "script2.py"]
    run_scripts_from_list(scripts)
    
    # Option 2: list in a file (one per line)
    run_scripts_from_file("scripts.txt")
