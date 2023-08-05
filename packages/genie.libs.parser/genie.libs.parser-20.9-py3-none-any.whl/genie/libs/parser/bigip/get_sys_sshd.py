# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/sys/sshd' resources
# =============================================


class SysSshdSchema(MetaParser):

    schema = {}


class SysSshd(SysSshdSchema):
    """ To F5 resource for /mgmt/tm/sys/sshd
    """

    cli_command = "/mgmt/tm/sys/sshd"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
