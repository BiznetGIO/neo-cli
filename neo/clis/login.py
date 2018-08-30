from neo.clis.base import Base
from neo.libs import login as login_lib
from neo.libs import utils
from tabulate import tabulate


class Login(Base):
    """
    Usage:
        login
        login -D | --describe
        login [-u USERNAME] [-k KEYSTONE-URL] [-d DOMAIN]


    Options:
    -h --help                                       Print usage
    -D --describe                                   Set your desired domain URL
    -k KEYSTONE-URL --keystone-url=KEYSTONE-URL     Set your desired keystone URL
    -d DOMAIN --domain=DOMAIN                       Set your desired domain URL
    -u USERNAME --username=USERNAME                 Set your desired username
    """

    def execute(self):
        if self.args["--describe"]:
            envs = login_lib.get_env_values()
            env_data = [[
                envs['username'],
                envs['auth_url'],
                envs['project_id'],
                envs['user_domain_name']
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

        if (self.args["--domain"] and self.args["--keystone-url"]):
            try:
                username = self.args['--username']
                auth_url = self.args['--keystone-url']
                user_domain_name = self.args['--domain']
                login_lib.do_login(auth_url=auth_url,
                                   user_domain_name=user_domain_name,
                                   username=username)
            except Exception as e:
                utils.log_err(e)

        if (not self.args["--domain"] and not self.args["--keystone-url"]):
            login_lib.do_login()
