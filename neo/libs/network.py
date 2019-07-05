from neo.libs import login as login_lib
from neutronclient.v2_0 import client as neutron_client
from neo.libs import utils


def get_neutron_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()
    neutron = neutron_client.Client(session=session)
    return neutron


def get_list(session=None):
    neutron = get_neutron_client(session)
    try:
        networks = neutron.list_networks()
    except Exception as e:
        utils.log_err(e)
    return networks["networks"]


def get_floatingips(session=None):
    neutron = get_neutron_client(session)
    try:
        floatingips = neutron.list_floatingips()
    except Exception as e:
        utils.log_err(e)
    return floatingips["floatingips"]


def do_delete(network_id, session=None):
    neutron = get_neutron_client(session)
    try:
        neutron.delete_network(network_id)
    except Exception as e:
        utils.log_err(e)


def list_sec_group(session=None):
    neutron = get_neutron_client(session)
    try:
        sec_group = neutron.list_security_groups()
    except Exception as e:
        utils.log_err(e)
    return sec_group["security_groups"]


def rules_sec_groups(sec_group, session=None):
    obj_sec_rule = list()
    neutron = get_neutron_client(session)
    try:
        sec_group = neutron.list_security_groups()["security_groups"]
    except Exception as e:
        utils.log_err(e)
    else:
        for i in sec_group:
            data = {"name": i["name"], "description": i["description"]}
            obj_sec_rule.append(data)
        return obj_sec_rule


def list_subnet(session=None):
    obj_subnet_list = list()
    neutron = get_neutron_client(session)
    try:
        obj_subnet_list = neutron.list_subnets()
    except Exception as e:
        utils.log_err(e)
    return obj_subnet_list


def show_subnet(subnet, session=None):
    obj_subnet = list()
    neutron = get_neutron_client(session)
    try:
        obj_subnet = neutron.show_subnet(subnet)
    except Exception as e:
        utils.log_err(e)
    return obj_subnet


def delete_subnet(subnet, session):
    neutron = get_neutron_client(session)
    try:
        return neutron.delete_subnet(subnet)
    except Exception as e:
        utils.log_err(e)


def list_router(session=None):
    obj_router_list = list()
    neutron = get_neutron_client(session)
    try:
        obj_router_list = neutron.list_routers()
    except Exception as e:
        utils.log_err(e)
    return obj_router_list


def show_router(routers, session=None):
    neutron = get_neutron_client(session)
    try:
        obj_router = neutron.show_router(routers)
    except Exception as e:
        utils.log_err(e)

    return obj_router


def delete_router(routers, session=None):
    neutron = get_neutron_client(session)
    try:
        return neutron.delete_router(routers)
    except Exception as e:
        utils.log_err(e)


def list_subnet_pool(session=None):
    obj_subnetpool_list = list()
    neutron = get_neutron_client(session)
    try:
        obj_subnetpool_list = neutron.list_subnetpools()
    except Exception as e:
        utils.log_err(e)

    return obj_subnetpool_list


def show_subnet_pool(subnetpool, session=None):
    neutron = get_neutron_client(session)
    try:
        obj_subnetpools = neutron.show_subnetpool(subnetpool)
    except Exception as e:
        utils.log_err(e)
    return obj_subnetpools


def delete_subnet_pool(subnetpool, session=None):
    neutron = get_neutron_client(session)
    try:
        return neutron.delete_subnetpool(subnetpool)
    except Exception as e:
        utils.log_err(e)


def list_port(session=None):
    obj_port_list = list()
    neutron = get_neutron_client(session)
    try:
        obj_port_list = neutron.list_ports()
    except Exception as e:
        utils.log_err(e)

    return obj_port_list


def show_port(port, session=None):
    neutron = get_neutron_client(session)
    try:
        obj_port = neutron.show_port(port)
    except Exception as e:
        utils.log_err(e)
    return obj_port


def delete_port(port, session=None):
    neutron = get_neutron_client(session)
    try:
        return neutron.delete_port(port)
    except Exception as e:
        utils.log_err(e)


def show_floatingips(floatingips, session=None):
    neutron = get_neutron_client(session)
    try:
        obj_floatingips = neutron.show_floatingip(floatingips)
    except Exception as e:
        utils.log_err(e)
    return obj_floatingips


def delete_floatingip(floatingips, session=None):
    neutron = get_neutron_client(session)
    try:
        return neutron.delete_floatingip(floatingips)
    except Exception as e:
        utils.log_err(e)
