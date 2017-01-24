import subprocess
import os
import xml.etree.ElementTree as et

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


def start_domain(connection_str, domain_name, snapshot_name):
    connection = libvirt.open("qemu+ssh://root@192.168.200.1/system")
    domain = connection.lookupByName(domain_name)
    snapshot = domain.snapshotLookupByName(snapshot_name)

    domain.revertToSnapshot(snapshot)
    domain.create()


def get_domains_and_snapshots(connection_str):
    all_domains = []
    connection = libvirt.open(connection_str)

    domain_names = connection.listDefinedDomains()
    for domain_name in domain_names:
        domain = connection.lookupByName(domain_name)
        for snapshot_name in domain.snapshotListNames():
            if not snapshot_name.lower().startswith("prod"):
                # only grep on prod
                continue

            # get the snapshot description
            snap = domain.snapshotLookupByName(snapshot_name)
            root = et.fromstring(snap.getXMLDesc())
            description = root.find("description")
            if description is not None:
                description = description.text

            entry = {"domain_name" : domain_name, "snapshot_name" : snapshot_name, "flag": str(description)}
            insert_str = "python3 ctf_db.py add_challenge {} {} {} ".format(domain_name, snapshot_name, str(description))

            print(insert_str)
            all_domains.append(entry)

    return all_domains
