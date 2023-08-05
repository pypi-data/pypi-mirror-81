# coding: utf-8

import pprint
import re

import six





class ShowAsyncDeviceCommandRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []
    sensitive_list.append('stage_auth_token')

    openapi_types = {
        'device_id': 'str',
        'stage_auth_token': 'str',
        'instance_id': 'str',
        'command_id': 'str'
    }

    attribute_map = {
        'device_id': 'device_id',
        'stage_auth_token': 'Stage-Auth-Token',
        'instance_id': 'Instance-Id',
        'command_id': 'command_id'
    }

    def __init__(self, device_id=None, stage_auth_token=None, instance_id=None, command_id=None):
        """ShowAsyncDeviceCommandRequest - a model defined in huaweicloud sdk"""
        
        

        self._device_id = None
        self._stage_auth_token = None
        self._instance_id = None
        self._command_id = None
        self.discriminator = None

        self.device_id = device_id
        if stage_auth_token is not None:
            self.stage_auth_token = stage_auth_token
        if instance_id is not None:
            self.instance_id = instance_id
        self.command_id = command_id

    @property
    def device_id(self):
        """Gets the device_id of this ShowAsyncDeviceCommandRequest.


        :return: The device_id of this ShowAsyncDeviceCommandRequest.
        :rtype: str
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        """Sets the device_id of this ShowAsyncDeviceCommandRequest.


        :param device_id: The device_id of this ShowAsyncDeviceCommandRequest.
        :type: str
        """
        self._device_id = device_id

    @property
    def stage_auth_token(self):
        """Gets the stage_auth_token of this ShowAsyncDeviceCommandRequest.


        :return: The stage_auth_token of this ShowAsyncDeviceCommandRequest.
        :rtype: str
        """
        return self._stage_auth_token

    @stage_auth_token.setter
    def stage_auth_token(self, stage_auth_token):
        """Sets the stage_auth_token of this ShowAsyncDeviceCommandRequest.


        :param stage_auth_token: The stage_auth_token of this ShowAsyncDeviceCommandRequest.
        :type: str
        """
        self._stage_auth_token = stage_auth_token

    @property
    def instance_id(self):
        """Gets the instance_id of this ShowAsyncDeviceCommandRequest.


        :return: The instance_id of this ShowAsyncDeviceCommandRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ShowAsyncDeviceCommandRequest.


        :param instance_id: The instance_id of this ShowAsyncDeviceCommandRequest.
        :type: str
        """
        self._instance_id = instance_id

    @property
    def command_id(self):
        """Gets the command_id of this ShowAsyncDeviceCommandRequest.


        :return: The command_id of this ShowAsyncDeviceCommandRequest.
        :rtype: str
        """
        return self._command_id

    @command_id.setter
    def command_id(self, command_id):
        """Sets the command_id of this ShowAsyncDeviceCommandRequest.


        :param command_id: The command_id of this ShowAsyncDeviceCommandRequest.
        :type: str
        """
        self._command_id = command_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ShowAsyncDeviceCommandRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
