from neo.clis.base import Base
from neo.libs import login as login_lib
from neo.libs import utils
from tabulate import tabulate


class Login(Base):
    """
    Usage:
        login
        login -D | --describe
        login [-u USERNAME] [-r REGION]


    Options:
    -h --help                                       Print usage
    -D --describe                                   Set your desired domain URL
    -r REGION --region=REGION                       Pick your region, to get list of region use neo --region      
    -u USERNAME --username=USERNAME                 Set your desired username
    """

    def execute(self):
        if self.args["--describe"]:
            envs = login_lib.get_env_values()
            try:
                env_data = []
                for env in envs:
                    data = [
                        env["username"],
                        env["region"],
                        env["auth_url"],
                        env["project_id"],
                        env["user_domain_name"],
                        env["status"],
                    ]
                    env_data.append(data)
            except:
                exit()

            if len(env_data) == 0:
                utils.log_err("No Data...")
                print(self.__doc__)
                exit()

            print(
                tabulate(
                    env_data,
                    headers=[
                        "Username",
                        "Region",
                        "Auth URL",
                        "Project ID",
                        "Domain Name",
                        "Status",
                    ],
                    tablefmt="grid",
                )
            )
            exit()

        if not self.args["--region"] and not self.args["--username"]:
            login_lib.do_login()
        else:
            login_lib.do_login(
                username=self.args["--username"], region=self.args["--region"]
            )
