import subprocess

KILL_VM_SCRIPT = "kill_shell.sh"


def kill_vms():
    print("killing shit with " + KILL_VM_SCRIPT)
    subprocess.call([KILL_VM_SCRIPT])
    print("killed?")
