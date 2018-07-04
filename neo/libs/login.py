import getpass
import os
import dill
from dotenv import load_dotenv
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from neo.libs import utils

home = os.path.expanduser("~")
auth_url = 'https://keystone.wjv-1.neo.id:443/v3'
user_domain_name = 'neo.id'


def get_username():
    return input("username: ")


def get_password():
    return getpass.getpass("password: ")


def generate_session(auth_url, username, password, **kwargs):
    auth = v3.Password(
        auth_url=auth_url,
        username=username,
        password=password,
        **kwargs)

    sess = session.Session(auth=auth)

    return sess


def check_env():
    return os.path.isfile("{}/.neo.env".format(home))


def create_env_file(username, password, project_id):
    try:
        env_file = open("{}/.neo.env".format(home), "w+")
        env_file.write("OS_USERNAME=%s\n" % username)
        env_file.write("OS_PASSWORD=%s\n" % password)
        env_file.write("OS_AUTH_URL=%s\n" % auth_url)
        env_file.write("OS_PROJECT_ID=%s\n" % project_id)
        env_file.write("OS_USER_DOMAIN_NAME=%s\n" % user_domain_name)
        env_file.close()
        return True
    except:
        return False


def add_token(token):
    try:
        env_file = open("{}/.neo.env".format(home), "a+")
        env_file.write("OS_TOKEN=%s\n" % token)
        env_file.close()
    except:
        return False


def load_env_file():
    return load_dotenv("{}/.neo.env".format(home), override=True)


def get_project_id(username, password):
    sess = generate_session(
        auth_url=auth_url,
        username=username,
        password=password,
        user_domain_name=user_domain_name)
    keystone = client.Client(session=sess)
    project_list = [
        t.id for t in keystone.projects.list(user=sess.get_user_id())
    ]

    return project_list[0]


def do_login():
    try:
        username = get_username()
        password = get_password()
        project_id = get_project_id(username, password)

        sess = generate_session(
            auth_url=auth_url,
            username=username,
            password=password,
            user_domain_name=user_domain_name,
            project_id=project_id,
            reauthenticate=True,
            include_catalog=True)

        set_session(sess)

        utils.log_info("Login Success")
        return True
    except Exception as e:
        utils.log_err(e)
        utils.log_err("Login Failed")
        return False


def do_logout():
    if check_session():
        os.remove('/tmp/session.pkl')
        utils.log_info("Logout Success")


def set_session(sess):
    try:
        with open('/tmp/session.pkl', 'wb') as f:
            dill.dump(sess, f)
    except Exception as e:
        utils.log_err("set session failed")


def get_session():
    try:
        sess = None
        with open('/tmp/session.pkl', 'rb') as f:
            sess = dill.load(f)
        return sess
    except Exception as e:
        print("you are not authorized")
        do_login()
        return get_session()


def check_session():
    return os.path.isfile("/tmp/session.pkl")
