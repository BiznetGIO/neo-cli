import git
import os
import yaml
import codecs
import shutil
import paramiko
import select
import npyscreen
import coloredlogs
import logging
import scp
import sys
import errno
import fcntl
import termios
import struct
import socket
# import traceback
import getpass
from binascii import hexlify
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from neo.libs import interactive_ssh_utils as interactive


def do_deploy_dir(manifest_file):
    try:
        manifest = {}
        manifest_dir = os.path.dirname(os.path.realpath(manifest_file))
        manifest["deploy_dir"] = "{}/.deploy".format(manifest_dir)

        if not os.path.isdir(manifest["deploy_dir"]):
            os.makedirs(manifest["deploy_dir"])

        key = get_key(manifest_file)
        manifest["stack"] = key["stack"]
        manifest["data"] = key["data"]

        return manifest

    except Exception as e:
        raise


def check_key(dict, val):
    try:
        if dict[val]:
            return True
    except Exception as e:
        return False


def question(word):
    answer = False
    while answer not in ["y", "n"]:
        answer = input("{} [y/n]? ".format(word)).lower().strip()

    if answer == "y":
        answer = True
    else:
        answer = False
    return answer


def get_index(dictionary):
    return [key for (key, value) in dictionary.items()]


def get_key(manifest_file):
    try:
        manifest = {
            "stack": {
                "services": [],
                "networks": [],
                "deployments": [],
                "clusters": [],
                "instances": [],
                "databases": [],
                "others": []
            }
        }

        neo_templates = codecs.open(
            manifest_file, encoding='utf-8', errors='strict')
        manifest["data"] = yaml.load(neo_templates.read())
        manifest_data = eval(str(manifest["data"]))
        del manifest_data["deploy"]
        for (key, value) in manifest_data.items():
            manifest["stack"][key] = [i for i, v in value.items()]
        return manifest

    except Exception as e:
        raise


def get_project(manifest_file):
    key = get_key(manifest_file)
    manifest = list()
    manifest += [service for service in key["stack"]["services"]]
    manifest += [network for network in key["stack"]["networks"]]
    manifest += [deploy for deploy in key["stack"]["deployments"]]
    manifest += [cluster for cluster in key["stack"]["clusters"]]
    manifest += [instance for instance in key["stack"]["instances"]]
    manifest += [database for database in key["stack"]["databases"]]
    manifest += [other for other in key["stack"]["others"]]

    return manifest


def template_git(url, dir):
    try:
        chk_repo = os.path.isdir(dir)
        if chk_repo:
            shutil.rmtree(dir)

        git.Repo.clone_from(url, dir)
        # real_url = os.path.dirname(os.path.realpath(dir))

        return True

    except Exception as e:
        return False


def template_url(url, dest):
    url_split = url.split("+")
    url_type = url_split[0]
    url_val = url_split[1]
    return {'git': template_git(url_val, dest), 'local': url_val}[url_type]


def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


def initdir(manifest):
    active_catalog = list()
    for (k, v) in manifest["stack"].items():
        stack_key = manifest["stack"][k]
        if len(stack_key) > 0:
            mkdir("{}/{}".format(manifest["deploy_dir"], k))
            active_catalog.append(k)
    return active_catalog


def repodata():
    abs_path = os.path.dirname(os.path.realpath(__file__))
    repo_file = "{}/templates/repo.yml".format(abs_path)
    return yaml_parser(repo_file)


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data

        except yaml.YAMLError as exc:
            print(exc)


def yaml_create(out_file, data):
    with open(out_file, 'w') as outfile:
        try:
            yaml.dump(data, outfile, default_flow_style=False)
            return True

        except yaml.YAMLError as exc:
            print(exc)


def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()


def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)


def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            listdir.append(os.path.join(root, file))
    return listdir


def terminal_size():
    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0,
                                                           0)))
    return tw, th


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """

    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        log_info('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
        try:
            transport.auth_publickey(username, key)
            log_info('... success!')
            return
        except paramiko.SSHException:
            log_err('... nope.')


def manual_auth(username, hostname, client):
    default_auth = 'p'
    try:
        auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' %
                     default_auth)
    except KeyboardInterrupt:
        sys.exit()

    if len(auth) == 0:
        auth = default_auth

    if auth == 'r':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        path = input('RSA key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path, password)
        client.auth_publickey(username, key)
    elif auth == 'd':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
        path = input('DSS key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.DSSKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('DSS key password: ')
            key = paramiko.DSSKey.from_private_key_file(path, password)
        client.auth_publickey(username, key)
    else:
        pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        client.auth_password(username, pw)


def ssh_connect(hostname,
                user,
                password=None,
                key_file=None,
                passphrase=None,
                socket=None):
    if key_file:
        neo_key = paramiko.RSAKey.from_private_key_file(
            filename=key_file, password=passphrase)
    else:
        neo_key = None

    if socket:
        client = paramiko.Transport(socket)
        try:
            client.start_client()
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)
        try:
            keys = paramiko.util.load_host_keys(
                os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(
                    os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print('*** Unable to open host keys file')
                keys = {}

        # check server's host key -- this is important.
        key = client.get_remote_server_key()
        if hostname not in keys:
            log_warn('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[hostname]:
            log_warn('*** WARNING: Unknown host key!')
        elif keys[hostname][key.get_name()] != key:
            log_warn('*** WARNING: Host key has changed!!!')
            sys.exit(1)
        else:
            log_info('*** Host key OK.')

        agent_auth(client, user)
        if not client.is_authenticated():
            if neo_key:
                client.auth_publickey(user, neo_key)
            elif password:
                client.auth_password(user, password)
            else:
                manual_auth(user, hostname, client)

        if not client.is_authenticated():
            log_err('*** Authentication failed. :(')
            client.close()
            sys.exit(1)
        return client

    else:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname, username=user, pkey=neo_key, password=password)
        log_info("Connected...")
        # Example : "tailf -n 50 /tmp/deploy.log"
        return client


def ssh_out_stream(hostname,
                   user,
                   commands,
                   password=None,
                   key_file=None,
                   passphrase=None):
    client = ssh_connect(
        hostname,
        user,
        password=password,
        key_file=key_file,
        passphrase=passphrase)
    channel = client.get_transport().open_session()
    # log_info("Connected...")
    # Example : "tailf -n 50 /tmp/deploy.log"
    channel.exec_command(commands)
    while True:
        if channel.exit_status_ready():
            break
        rl, wl, xl = select.select([channel], [], [], 0.0)
        if len(rl) > 0:
            print(channel.recv(1024).decode("utf-8"))


def ssh_shell(hostname,
              user,
              password=None,
              port=22,
              key_file=None,
              passphrase=None):
    try:
        port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        # traceback.print_exc()
        exit(0)

    client = ssh_connect(
        hostname,
        user,
        password=password,
        key_file=key_file,
        passphrase=passphrase,
        socket=sock)
    chan = client.open_session()
    w_size, h_size = terminal_size()
    chan.get_pty(width=w_size, height=h_size)
    chan.invoke_shell()
    interactive.interactive_shell(chan)
    chan.close()


"""
    Put all file from directory to remote servers
    scp_put(str(hostname),str(user),list(source_files),
    str(destination_to_remoteserver),str(password),str(key file),
    str(key passphrase))
    Examples :
    scp_put("192.168.0.1","user",list_dir("."),"/home/user",key_file="key.pem")
    or
    scp_put("192.168.0.1","user",list_dir("."),"/home/user",password="mypassword")
"""


def scp_put(hostname,
            user,
            source_files,
            destination_folder,
            password=None,
            key_file=None,
            passphrase=None):
    client = ssh_connect(
        hostname,
        user,
        password=password,
        key_file=key_file,
        passphrase=passphrase)
    """ Define progress callback that prints the current percentage completed
    for the file """

    def progress(filename, size, sent):
        sys.stdout.write("upload progress: %.2f%%   \r" %
                         (float(sent) / float(size) * 100))

    scp_client = scp.SCPClient(client.get_transport(), progress=progress)
    sftp_client = paramiko.SFTPClient.from_transport(client.get_transport())
    for sf in source_files:
        if os.path.isfile(sf):
            try:
                remote_file = os.path.join(destination_folder, sf)
                file_dir = os.path.dirname(remote_file)
                sftp_client.stat(remote_file)
            except IOError as e:
                if e.errno == errno.ENOENT:
                    channel = client.get_transport().open_session()
                    channel.exec_command('mkdir -p {}'.format(file_dir))
                    scp_client.put(
                        sf,
                        remote_file,
                        recursive=True,
                    )
            else:
                scp_client.put(
                    sf,
                    remote_file,
                    recursive=True,
                )
            finally:
                print(str(sf))
        else:
            log_err('file not found')
    scp_client.close()
    sftp_client.close()


"""
Generate text user interface:

example :
fields = [
    {"type": "TitleText", "name": "Name", "key": "name"},
    {"type": "TitlePassword", "name": "Password", "key": "password"},
    {"type": "TitleSelectOne", "name": "Role",
        "key": "role", "values": ["admin", "user"]},
]

form = form_generator("Form Instalasi", fields)
print(form["role"].value[0])
print(form["name"].value)

"""


def form_generator(form_title, fields):
    def myFunction(*args):
        form = npyscreen.Form(name=form_title)
        result = {}
        for field in fields:
            t = field["type"]
            k = field["key"]
            del field["type"]
            del field["key"]

            result[k] = form.add(getattr(npyscreen, t), **field)
        form.edit()
        return result

    return npyscreen.wrapper_basic(myFunction)


def prompt_generator(form_title, fields):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(form_title)

    data = {}
    for field in fields:
        if field['type'] == 'TitleSelectOne':
            print('{} : '.format(field['name']))
            completer = WordCompleter(field['values'], ignore_case=True)
            for v in field['values']:
                print('- {}'.format(v))
            text = None

            while text not in field['values']:
                text = prompt('Enter your choice : ', completer=completer)

            data[field['key']] = text
        elif field['type'] == 'TitleSelect':
            print('{} : '.format(field['name']))
            completer = WordCompleter(field['values'], ignore_case=True)
            for v in field['values']:
                print('- {}'.format(v))
            data[field['key']] = prompt(
                'Enter your choice or create new : ', completer=completer)
        elif field['type'] == 'TitlePassword':
            data[field['key']] = prompt(
                '{} : '.format(field['name']), is_password=True)
        else:
            data[field['key']] = prompt('{} : '.format(field['name']))
        print('------------------------------')
    return data


def isint(number):
    try:
        to_float = float(number)
        to_int = int(to_float)
    except ValueError:
        return False
    else:
        return to_float == to_int


def isfloat(number):
    try:
        float(number)
    except ValueError:
        return False
    else:
        return True
