from neo.libs import login as login_lib
from glanceclient import Client as image_client


def get_image_client(session=None):
    if not session:
        session = login_lib.get_session()
    img = image_client('2', session=session)
    return img


def get_list(session=None):
    img = get_image_client(session)
    return img.images.list()


def detail(image_id, session=None):
    img = get_image_client(session)
    return img.images.get(image_id)
