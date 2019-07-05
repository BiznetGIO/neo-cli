from neo.libs import login as login_lib
from novaclient import client as nova_client
from neo.libs import utils


def get_nova_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()

    compute = nova_client.Client(2, session=session)
    return compute


def get_list(session=None):
    compute = get_nova_client(session)
    try:
        instances = [instance for instance in compute.servers.list()]
    except Exception as e:
        utils.log_err(e)

    return instances


def detail(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.get(vm_id)
    except Exception as e:
        utils.log_err(e)


def do_delete(instance_id, session=None):
    compute = get_nova_client(session)
    compute.servers.delete(instance_id)


def get_flavor(session=None):
    compute = get_nova_client(session)
    try:
        return compute.flavors.list()
    except Exception as e:
        utils.log_err(e)


def detail_flavor(flavor_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.flavors.get(flavor_id)
    except Exception as e:
        utils.log_err(e)


def get_keypairs(session=None):
    compute = get_nova_client(session)
    try:
        return compute.keypairs.list()
    except Exception as e:
        utils.log_err(e)


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
    try:
        return compute.servers.suspend(vm_id)
    except Exception as e:
        utils.log_err(e)


def resume(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.resume(vm_id)
    except Exception as e:
        utils.log_err(e)


def lock(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.lock(vm_id)
    except Exception as e:
        utils.log_err(e)


def unlock(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.unlock(vm_id)
    except Exception as e:
        utils.log_err(e)


def resize(vm_id, flavor, session=None):
    compute = get_nova_client(session)
    try:
        return compute.resize(vm_id, flavor=flavor)
    except Exception as e:
        utils.log_err(e)


def confirm_size(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.confirm_resize(vm_id)
    except Exception as e:
        utils.log_err(e)


def revert_size(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.revert_resize(vm_id)
    except Exception as e:
        utils.log_err(e)


def attach_interface(vm_id, port_id, net_id, fixed_ip, session=None):
    compute = get_nova_client(session)
    try:
        attach_ip = compute.servers.interface_attach(
            vm_id, port_id, net_id, fixed_ip, tag=None
        )
    except Exception as e:
        utils.log_err(e)
    return attach_ip


def detach_interface(vm_id, port_id, session=None):
    compute = get_nova_client(session)
    try:
        detach_ip = compute.servers.interface_detach(vm_id, port_id)
    except Exception as e:
        utils.log_err(e)
    return detach_ip


def get_vnc_console_url(vm_id, vnc_type, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.get_vnc_console(vm_id, vnc_type)
    except Exception as e:
        utils.log_err(e)


def pause_instance(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.pause(vm_id)
    except Exception as e:
        utils.log_err(e)


def unpause_instance(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.unpause(vm_id)
    except Exception as e:
        utils.log_err(e)


def start_instance(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.start(vm_id)
    except Exception as e:
        utils.log_err(e)


def stop_instance(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.stop(vm_id)
    except Exception as e:
        utils.log_err(e)


def reboot_instance(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.reboot(vm_id)
    except Exception as e:
        utils.log_err(e)


def restore_instance(vm_id, session=None):
    compute = get_nova_client(session)
    try:
        return compute.servers.restore(vm_id)
    except Exception as e:
        utils.log_err(e)


def action_logs(vm_id, session=None):
    compute = get_nova_client(session)
    log_action = list()
    try:
        log_action = compute.instance_action.list(vm_id)
    except Exception as e:
        utils.log_err(e)
    return log_action


def action_logs_show(vm_id, action_id, session=None):
    compute = get_nova_client(session)
    detail_action = list()
    try:
        detail_action = compute.instance_action.get(vm_id, action_id)
    except Exception as e:
        utils.log_err(e)
    return detail_action
