from neo.clis.base import Base
from neo.libs import login as login_lib


class Login(Base):
    """
    Usage:
        login
        login [-u KEYSTONE-URL] [-d DOMAIN]


    Options:
    -h --help                                             Print usage
    -u KEYSTONE-URL --keystone-url=KEYSTONE-URL           Set your desired keystone URL
    -d DOMAIN --domain=DOMAIN                             Set your desired domain URL

    """

    def execute(self):
        if self.args["--domain"] and self.args["--keystone-url"]:
            try:
                auth_url = self.args['--keystone-url']
                domain_url = self.args['--domain']
                login_lib.do_login(auth_url, domain_url)
            except Exception as e:
                utils.log_err(e)

        return login_lib.do_login()
