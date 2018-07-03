from neo.libs import login as login_lib
from neutronclient.v2_0 import client as neutron_client


def get_neutron_client(session=None):
    if not session:
        session = login_lib.get_session()
    neutron = neutron_client.Client(session=session)
    return neutron


def get_list(session=None):
    neutron = get_neutron_client(session)
    networks = neutron.list_networks()
    return networks['networks']


def do_delete(network_id, session=None):
    neutron = get_neutron_client(session)
    neutron.delete_network(network_id)
