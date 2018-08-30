from neo.clis.base import Base
from neo.libs import login as login_lib
from neo.libs import utils
from tabulate import tabulate


class Login(Base):
    """
    Usage:
        login
        login -D | --describe
        login [-u KEYSTONE-URL] [-d DOMAIN]


    Options:
    -h --help                                       Print usage
    -D --describe                                   Set your desired domain URL
    -k KEYSTONE-URL --keystone-url=KEYSTONE-URL     Set your desired keystone URL
    -d DOMAIN --domain=DOMAIN                       Set your desired domain URL
    -u USERNAME --user=USERNAME                     Set your desired username
    """

    def execute(self):
        if self.args["--describe"]:
            envs = login_lib.get_env_values()
            env_data = [[
                envs['username'],
                envs['auth_url'],
                envs['project_id'],
                envs['domain_name']
            ]]
            if len(env_data) == 0:
                utils.log_err("No Data...")
                print(self.__doc__)
                exit()
            print(
                tabulate(
                    env_data,
                    headers=["Username", "Auth URL", "Project ID",
                             "Domain Name"],
                    tablefmt="grid"))
            exit()

        if self.args["--domain"] and self.args["--keystone-url"]:
            try:
                custom_auth_url = self.args['--keystone-url']
                custom_domain_url = self.args['--domain']
                username = self.args['--user']
                login_lib.do_login(custom_auth_url, custom_domain_url,
                                   username)
            except Exception as e:
                utils.log_err(e)

        login_lib.do_login()
