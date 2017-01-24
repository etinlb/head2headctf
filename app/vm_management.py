import subprocess
import os

KILL_VM_SCRIPT = "kill_shell.sh"

def kill_vms():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script = os.path.join(dir_path, KILL_VM_SCRIPT)
    print("killing shit with " + script)
    subprocess.call([script])
    print("killed?")
