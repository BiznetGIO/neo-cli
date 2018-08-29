import getpass
import os
import dill
from dotenv import load_dotenv
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from neo.libs import utils

GLOBAL_HOME = os.path.expanduser("~")
GLOBAL_AUTH_URL = 'https://keystone.wjv-1.neo.id:443/v3'
GLOBAL_USER_DOMAIN_NAME = 'neo.id'


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
    return os.path.isfile("{}/.neo.env".format(GLOBAL_HOME))


def create_env_file(username, password, project_id,
                    auth_url, domain_name):
    try:
        env_file = open("{}/.neo.env".format(GLOBAL_HOME), "w+")
        env_file.write("OS_USERNAME=%s\n" % username)
        env_file.write("OS_PASSWORD=%s\n" % password)
        env_file.write("OS_AUTH_URL=%s\n" % auth_url)
        env_file.write("OS_PROJECT_ID=%s\n" % project_id)
        env_file.write("OS_USER_DOMAIN_NAME=%s\n" % domain_name)
        env_file.close()
        return True
    except Exception as e:
        utils.log_err(e)
        return False


def load_env_file():
    return load_dotenv("{}/.neo.env".format(GLOBAL_HOME), override=True)


def get_env_values():
    if check_env():
        load_env_file()
        neo_env = {}
        neo_env['username'] = os.environ.get('OS_USERNAME')
        neo_env['password'] = os.environ.get('OS_PASSWORD')
        neo_env['auth_url'] = os.environ.get('OS_AUTH_URL')
        neo_env['project_id'] = os.environ.get('OS_PROJECT_ID')
        neo_env['domain_name'] = os.environ.get('OS_USER_DOMAIN_NAME')
        return neo_env
    else:
        utils.log_err("Can't find neo.env")


def get_project_id(username, password, auth_url, domain_name):
    sess = generate_session(
        auth_url=auth_url,
        username=username,
        password=password,
        user_domain_name=domain_name)
    keystone = client.Client(session=sess)
    project_list = [
        t.id for t in keystone.projects.list(user=sess.get_user_id())
    ]

    return project_list[0]


def is_current_env(auth_url, domain_name):
    """ check if auth_url and domain_name differ from current .neo.env"""
    envs = get_env_values()
    if envs['auth_url'] == auth_url and envs['domain_name'] == domain_name:
        return True
    else:
        return False


def do_login(auth_url=GLOBAL_AUTH_URL,
             domain_name=GLOBAL_USER_DOMAIN_NAME):
    try:
        print('auth_url: ' + auth_url)
        print('domain_name: ' + domain_name)
        if is_current_env(auth_url, domain_name):
            # regenerate session from current .neo.env
            print("Retrievingeving last login info ...")
            envs = get_env_values()
            set_session(collect_session_values(envs['username'],
                                               envs['password'],
                                               envs['project_id']))
            utils.log_info("Login Success")
            return True
        else:
            print("You are using new account")
            username = get_username()
            password = get_password()
            project_id = get_project_id(username, password, auth_url,
                                        domain_name)
            # create new session
            sess = collect_session_values(
                username, password,
                project_id,
                auth_url,
                domain_name)
            set_session(sess)

            # override env
            create_env_file(username, password, project_id, auth_url,
                            domain_name)
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


def collect_session_values(username, password,
                           project_id, auth_url=GLOBAL_AUTH_URL,
                           domain_name=GLOBAL_USER_DOMAIN_NAME):
    sess = generate_session(
        auth_url=auth_url,
        username=username,
        password=password,
        user_domain_name=domain_name,
        project_id=project_id,
        reauthenticate=True,
        include_catalog=True)
    return sess


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
        utils.log_err("Loading Session Failed")
        utils.log_err(e)


def check_session():
    return os.path.isfile("/tmp/session.pkl")
