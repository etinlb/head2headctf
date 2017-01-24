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

def get_domains_and_snapshots(connection_str):
    all_domains = []
    connection = libvirt.open(connection_str)

    domain_names = connection.listDefinedDomains(domain_name)
    for domain_name in domain_names:
        domain = connection.lookupByName(domain_name)
        for snapshot in domain.snapshotListNames():
            entry = {"domain_name" : domain_name, "snapshot_name" : snapshot}
            insert_str = "python3 ctf_db.py add_challenge {} {} <flag1> ".format(domain_name, snapshot_name)
            print(insert_str)
            all_domains.append(entry)

    return all_domains


