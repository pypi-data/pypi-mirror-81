# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/ltm/profile/statistics' resources
# =============================================


class LtmProfileStatisticsSchema(MetaParser):

    schema = {}


class LtmProfileStatistics(LtmProfileStatisticsSchema):
    """ To F5 resource for /mgmt/tm/ltm/profile/statistics
    """

    cli_command = "/mgmt/tm/ltm/profile/statistics"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
