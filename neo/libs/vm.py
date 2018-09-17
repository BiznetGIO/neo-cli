from neo.libs import login as login_lib
from novaclient import client as nova_client


def get_nova_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()

    compute = nova_client.Client(2, session=session)
    return compute


def get_list(session=None):
    compute = get_nova_client(session)
    instances = [instance for instance in compute.servers.list()]
    return instances


def detail(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.get(vm_id)


def do_delete(instance_id, session=None):
    compute = get_nova_client(session)
    compute.servers.delete(instance_id)


def get_flavor(session=None):
    compute = get_nova_client(session)
    return compute.flavors.list()


def detail_flavor(flavor_id, session=None):
    compute = get_nova_client(session)
    return compute.flavors.get(flavor_id)


def get_keypairs(session=None):
    compute = get_nova_client(session)
    return compute.keypairs.list()


def get_console_logs(instance_id, length=None, session=None):
    compute = get_nova_client(session)
    logs = None
    if length:
        logs = compute.servers.get_console_output(instance_id, length=length)
    else:
        logs = compute.servers.get_console_output(instance_id)
    return logs


def suspend(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.suspend(vm_id)


def resume(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.resume(vm_id)


def lock(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.lock(vm_id)


def unlock(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.unlock(vm_id)


def resize(vm_id, flavor, session=None):
    compute = get_nova_client(session)
    return compute.resize(id, flavor=flavor)


def confirm_size(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.confirm_resize(vm_id)


def revert_size(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.revert_resize(vm_id)


def attach_interface(vm_id, port_id, net_id, fixed_ip, session=None):
    compute = get_nova_client(session)
    attach_ip = compute.servers.interface_attach(
                        id,
                        port_id,
                        net_id,
                        fixed_ip,
                        tag=None
                    )
    return attach_ip


def detach_interface(vm_id, port_id, session=None):
    compute = get_nova_client(session)
    detach_ip = compute.servers.interface_detach(vm_id, port_id)
    return detach_ip


def get_vnc_console_url(vm_id, vnc_type, session=None):
    compute = get_nova_client(session)
    return compute.servers.get_vnc_console(vm_id, vnc_type)


def pause_instance(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.pause(vm_id)


def unpause_instance(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.unpause(vm_id)
