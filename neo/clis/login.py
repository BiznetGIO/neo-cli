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
    -u KEYSTONE-URL --keystone-url=KEYSTONE-URL     Set your desired keystone URL
    -d DOMAIN --domain=DOMAIN                       Set your desired domain URL

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
                auth_url = self.args['--keystone-url']
                domain_url = self.args['--domain']
                login_lib.do_login(auth_url, domain_url)
            except Exception as e:
                utils.log_err(e)

        login_lib.do_login()
