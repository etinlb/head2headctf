import subprocess
import os
try:
    import libvirt
except Exception as e:
    pass

KILL_VM_SCRIPT = "kill_shell.sh"

def kill_vms():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script = os.path.join(dir_path, KILL_VM_SCRIPT)
    print("killing shit with " + script)
    subprocess.call([script])
    print("killed?")


def start_domain(connection_str, domain_name, snap_shot_name):
    connection = libvirt.open("qemu+ssh://root@192.168.200.1/system")
    domain = connection.lookupByName(domain_name)
    snapshot = domain.snapshotLookupByName(snap_shot_name)

    domain.revertToSnapshot(snapshot)
    domain.create()


