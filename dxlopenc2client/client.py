from __future__ import absolute_import
from dxlclient.message import Request, Message
from dxlbootstrap.util import MessageUtils
from dxlbootstrap.client import Client

import openc2


class OpenC2Client(Client):
    """
    The "DXL OpenC2 Client" client wrapper class.
    """

    def __init__(self, dxl_client): # pylint: disable=useless-super-delegation
        """
        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the fabric
        """
        super(OpenC2Client, self).__init__(dxl_client)

    def send_command(self, topic, command):
        # Create the DXL request message
        request = Request(topic)

        # Serialize and encode the OpenC2 command
        request.payload = command.serialize().encode()

        # Perform a synchronous DXL request
        response = self._dxl_sync_request(request)

        if response.message_type == Message.MESSAGE_TYPE_ERROR:
            raise Exception(response.error_message)

        # Return the response
        response_dict = MessageUtils.json_payload_to_dict(response)
        return openc2.v10.Response(**response_dict)
