from neo.libs import login as login_lib
from glanceclient import Client as image_client
from neo.libs import utils


def get_image_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()
    img = image_client("2", session=session)
    return img


def get_list(session=None):
    img = get_image_client(session)
    img_list = list()
    try:
        img_list = img.images.list()
    except Exception:
        return None
    return img_list


def detail(image_id, session=None):
    img = get_image_client(session)
    try:
        return img.images.get(image_id)
    except Exception:
        return None
