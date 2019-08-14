from neo.libs import login as login_lib
from neo.libs import utils
from cinderclient import client as cinder_client


def get_cinder_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()

    storage = cinder_client.Client(2, session=session)
    return storage


def get_list(session=None):
    storage = get_cinder_client(session)
    list_storage = [i for i in storage.volumes.list()]
    return list_storage


def detail(vol_id, session=None):
    storage = get_cinder_client(session)
    details = storage.volumes.get(vol_id)
    return details


def do_delete(vol_id, session=None):
    storage = get_cinder_client(session)
    try:
        storage.volumes.delete(vol_id)
    except Exception as e:
        utils.log_err("Volumes Not Delete : " + str(e))
        return 0
    else:
        return 1
