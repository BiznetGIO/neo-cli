from neo.libs import login as login_lib
from neutronclient.v2_0 import client as neutron_client


def get_neutron_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()
    neutron = neutron_client.Client(session=session)
    return neutron


def get_list(session=None):
    neutron = get_neutron_client(session)
    networks = neutron.list_networks()
    return networks['networks']


def get_floatingips(session=None):
    neutron = get_neutron_client(session)
    floatingips = neutron.list_floatingips()
    return floatingips['floatingips']


def do_delete(network_id, session=None):
    neutron = get_neutron_client(session)
    neutron.delete_network(network_id)


def list_sec_group(session=None):
    neutron = get_neutron_client(session)
    sec_group =  neutron.list_security_groups()
    return sec_group['security_groups']


def rules_sec_groups(sec_group, session=None):
    obj_sec_rule = list()
    neutron = get_neutron_client(session)
    sec_group =  neutron.list_security_groups()
    sec_group = sec_group['security_groups']
    for i in sec_group:
        data = {
            'name': i['name'],
            'description': i['description']
        }
        obj_sec_rule.append(data)
    return obj_sec_rule


def list_subnet(session=None):
    obj_subnet_list = list()
    neutron = get_neutron_client(session)
    obj_subnet_list = neutron.list_subnets()
    return obj_subnet_list


def show_subnet(subnet, session=None):
    obj_subnet = list()
    neutron = get_neutron_client(session)
    obj_subnet = neutron.show_subnet(subnet)
    return obj_subnet

def delete_subnet(subnet, session):
    neutron = get_neutron_client(session)
    return neutron.delete_subnet(subnet)


def list_router(session=None):
    obj_router_list = list()
    neutron = get_neutron_client(session)
    obj_router_list = neutron.list_routers()
    return obj_router_list


def show_router(routers, session=None):
    neutron = get_neutron_client(session)
    obj_router = neutron.show_router(routers)
    return obj_router


def delete_router(routers, session=None):
    neutron = get_neutron_client(session)
    return neutron.delete_router(routers)


def list_subnet_pool(session=None):
    obj_subnetpool_list = list()
    neutron = get_neutron_client(session)
    obj_subnetpool_list = neutron.list_subnetpools()
    return obj_subnetpool_list


def show_subnet_pool(subnetpool, session=None):
    neutron = get_neutron_client(session)
    obj_subnetpools = neutron.show_subnetpool(subnetpool)
    return 


def delete_subnet_pool(subnetpool, session=None):
    neutron = get_neutron_client(session)
    return neutron.delete_subnetpool(subnetpool)