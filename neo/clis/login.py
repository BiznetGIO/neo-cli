from neo.clis.base import Base
from neo.libs import login as login_lib


class Login(Base): 
    """
    usage:
        login
        login [-u KEYSTONE-URL] [-d DOMAIN]

    List all stack

    Options:
    -h --help                                                     Print usage
    -u KEYSTONE-URL --keystone-url=KEYSTONE-URL                   Set neo manifest file
    -d DOMAIN --domain=DOMAIN                                     Print outputs from stack name

    Log in to Neo Cloud
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
