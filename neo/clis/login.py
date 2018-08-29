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
        try:
            auth_url = self.args['--keystone-url']
        except Exception as e:
            auth_url = None
        try:
            domain_url = self.args['--domain']
        except Exception as e:
            domain_url = None

        login_lib.do_login(keystone_url=auth_url, domain_name=domain_url)
