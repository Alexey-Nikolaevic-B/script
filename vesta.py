import subprocess
import os

def open_vesta(vesta_path):
    if os.path.exists(vesta_path) and os.access(vesta_path, os.X_OK):
        process = subprocess.Popen([vesta_path])
        print("VESTA started successfully")
    else:
        print("VESTA executable not found or not executable")
        try:
            os.chmod(vesta_path, 0o755)
            process = subprocess.Popen([vesta_path])
            print("VESTA started after making it executable")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":

    vesta_path = "./VESTA-gtk3/VESTA"
    open_vesta(vesta_path)