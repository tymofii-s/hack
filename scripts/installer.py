import subprocess

libraries = ["pywin32", "pycryptodomex"]

def is_library_installed(lib):
    try:
        # Call "pip show" to check for library availability, without output to the console
        subprocess.check_output(["pip", "show", lib], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def install_libraries(lib_list):
    for lib in lib_list:
        if is_library_installed(lib):
            print(f"{lib} already installed.")
        else:
            try:
                subprocess.check_call(["pip", "install", lib])
                print(f"{lib} installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Installation error {lib}: {e}")

install_libraries(libraries)