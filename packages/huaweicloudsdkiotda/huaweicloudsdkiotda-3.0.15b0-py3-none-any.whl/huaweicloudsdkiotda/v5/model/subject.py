# coding: utf-8

import pprint
import re

import six





class Subject:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'resource': 'str',
        'event': 'str'
    }

    attribute_map = {
        'resource': 'resource',
        'event': 'event'
    }

    def __init__(self, resource=None, event=None):
        """Subject - a model defined in huaweicloud sdk"""
        
        

        self._resource = None
        self._event = None
        self.discriminator = None

        self.resource = resource
        self.event = event

    @property
    def resource(self):
        """Gets the resource of this Subject.

        订阅的资源名称。 - device：设备。 - device.data：设备数据。 - device.message.status：设备消息状态。 - device.status：设备状态。 - batchtask.status：批量任务状态。 

        :return: The resource of this Subject.
        :rtype: str
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """Sets the resource of this Subject.

        订阅的资源名称。 - device：设备。 - device.data：设备数据。 - device.message.status：设备消息状态。 - device.status：设备状态。 - batchtask.status：批量任务状态。 

        :param resource: The resource of this Subject.
        :type: str
        """
        self._resource = resource

    @property
    def event(self):
        """Gets the event of this Subject.

        订阅的资源事件，取值范围：activate、update、up。 event需要与resource关联使用，具体的“resource：event”映射关系如下： - device：activate（设备激活） - device.data：update（设备数据变化） - device.message.status：update（设备消息状态） - device.status：update （设备状态变化） - batchtask.status：update （批量任务状态变化） 

        :return: The event of this Subject.
        :rtype: str
        """
        return self._event

    @event.setter
    def event(self, event):
        """Sets the event of this Subject.

        订阅的资源事件，取值范围：activate、update、up。 event需要与resource关联使用，具体的“resource：event”映射关系如下： - device：activate（设备激活） - device.data：update（设备数据变化） - device.message.status：update（设备消息状态） - device.status：update （设备状态变化） - batchtask.status：update （批量任务状态变化） 

        :param event: The event of this Subject.
        :type: str
        """
        self._event = event

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
        if not isinstance(other, Subject):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
