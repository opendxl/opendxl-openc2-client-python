from __future__ import absolute_import
from dxlclient.message import Request, Message
from dxlbootstrap.util import MessageUtils
from dxlbootstrap.client import Client

import openc2


class OpenC2Client(Client):
    """
    The Open Command and Control (OpenC2) client wrapper class.
    """

    def __init__(self, dxl_client): # pylint: disable=useless-super-delegation
        """
        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the fabric
        """
        super(OpenC2Client, self).__init__(dxl_client)

    def send_command(self, topic, command):
        """
        Sends an Open Command and Control (OpenC2) message to the
        specified DXL service and returns the response.

        The `Lycan library <https://github.com/oasis-open/openc2-lycan-python>`_
        contains the OpenC2 classes (Command, Response, etc.).

        :param topic: The DXL service topic to send the OpenC2 command to
        :param command: The `openc2.v10.Command` to send to the DXL service
        :return: The `openc2.v10.Response` received from the DXL service
        """

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
