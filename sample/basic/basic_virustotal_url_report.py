from __future__ import absolute_import
import os
import sys

import openc2
import stix2

from dxlbootstrap.util import MessageUtils
from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir + "/../..")
sys.path.append(root_dir + "/..")

from dxlopenc2client.client import OpenC2Client

# Import common logging and configuration
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as dxl_client:

    # Connect to the fabric
    dxl_client.connect()

    logger.info("Connected to DXL fabric.")

    # Create client wrapper
    client = OpenC2Client(dxl_client)

    # Custom Actuator (VirusTotal)
    @openc2.v10.CustomActuator(
        "x-virustotal", [
            ("resource", stix2.properties.StringProperty(required=True))
        ]
    )
    class VirusTotalActuator(object):  # pylint: disable=useless-object-inheritance
        pass

    # Send the command and receive the response
    cmd = openc2.v10.Command(
        action="query",
        target=openc2.v10.Properties(properties=["url-report"]),
        actuator=VirusTotalActuator(resource="https://docs.oasis-open.org/")
    )
    response = client.send_command('/openc2-virustotal/service/api', cmd)
    response_dict = MessageUtils.json_to_dict(response.serialize())

    # Print out the response (convert dictionary to JSON for pretty printing)
    print("Response:\n{0}".format(
        MessageUtils.dict_to_json(response_dict, pretty_print=True)))
