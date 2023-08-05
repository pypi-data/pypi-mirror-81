# coding: utf-8

import pprint
import re

import six





class DeviceCommandRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'service_id': 'str',
        'command_name': 'str',
        'paras': 'object'
    }

    attribute_map = {
        'service_id': 'service_id',
        'command_name': 'command_name',
        'paras': 'paras'
    }

    def __init__(self, service_id=None, command_name=None, paras=None):
        """DeviceCommandRequest - a model defined in huaweicloud sdk"""
        
        

        self._service_id = None
        self._command_name = None
        self._paras = None
        self.discriminator = None

        if service_id is not None:
            self.service_id = service_id
        if command_name is not None:
            self.command_name = command_name
        self.paras = paras

    @property
    def service_id(self):
        """Gets the service_id of this DeviceCommandRequest.

        设备命令所属的设备服务ID，在设备关联的产品模型中定义。

        :return: The service_id of this DeviceCommandRequest.
        :rtype: str
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        """Sets the service_id of this DeviceCommandRequest.

        设备命令所属的设备服务ID，在设备关联的产品模型中定义。

        :param service_id: The service_id of this DeviceCommandRequest.
        :type: str
        """
        self._service_id = service_id

    @property
    def command_name(self):
        """Gets the command_name of this DeviceCommandRequest.

        设备命令名称，在设备关联的产品模型中定义。

        :return: The command_name of this DeviceCommandRequest.
        :rtype: str
        """
        return self._command_name

    @command_name.setter
    def command_name(self, command_name):
        """Sets the command_name of this DeviceCommandRequest.

        设备命令名称，在设备关联的产品模型中定义。

        :param command_name: The command_name of this DeviceCommandRequest.
        :type: str
        """
        self._command_name = command_name

    @property
    def paras(self):
        """Gets the paras of this DeviceCommandRequest.

        设备执行的命令，Json格式，里面是一个个健值对，如果serviceId不为空，每个健都是profile中命令的参数名（paraName）;如果serviceId为空则由用户自定义命令格式。设备命令示例：{\"value\":\"1\"}，具体格式需要应用和设备约定。 

        :return: The paras of this DeviceCommandRequest.
        :rtype: object
        """
        return self._paras

    @paras.setter
    def paras(self, paras):
        """Sets the paras of this DeviceCommandRequest.

        设备执行的命令，Json格式，里面是一个个健值对，如果serviceId不为空，每个健都是profile中命令的参数名（paraName）;如果serviceId为空则由用户自定义命令格式。设备命令示例：{\"value\":\"1\"}，具体格式需要应用和设备约定。 

        :param paras: The paras of this DeviceCommandRequest.
        :type: object
        """
        self._paras = paras

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
        if not isinstance(other, DeviceCommandRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
