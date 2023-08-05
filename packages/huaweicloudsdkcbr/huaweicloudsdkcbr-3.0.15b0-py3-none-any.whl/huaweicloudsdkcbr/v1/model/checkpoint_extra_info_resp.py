# coding: utf-8

import pprint
import re

import six





class CheckpointExtraInfoResp:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'name': 'str',
        'description': 'str',
        'retention_duration': 'int'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'retention_duration': 'retention_duration'
    }

    def __init__(self, name=None, description=None, retention_duration=None):
        """CheckpointExtraInfoResp - a model defined in huaweicloud sdk"""
        
        

        self._name = None
        self._description = None
        self._retention_duration = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if retention_duration is not None:
            self.retention_duration = retention_duration

    @property
    def name(self):
        """Gets the name of this CheckpointExtraInfoResp.

        备份名称

        :return: The name of this CheckpointExtraInfoResp.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CheckpointExtraInfoResp.

        备份名称

        :param name: The name of this CheckpointExtraInfoResp.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """Gets the description of this CheckpointExtraInfoResp.

        备份描述

        :return: The description of this CheckpointExtraInfoResp.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CheckpointExtraInfoResp.

        备份描述

        :param description: The description of this CheckpointExtraInfoResp.
        :type: str
        """
        self._description = description

    @property
    def retention_duration(self):
        """Gets the retention_duration of this CheckpointExtraInfoResp.

        备份保留天数

        :return: The retention_duration of this CheckpointExtraInfoResp.
        :rtype: int
        """
        return self._retention_duration

    @retention_duration.setter
    def retention_duration(self, retention_duration):
        """Sets the retention_duration of this CheckpointExtraInfoResp.

        备份保留天数

        :param retention_duration: The retention_duration of this CheckpointExtraInfoResp.
        :type: int
        """
        self._retention_duration = retention_duration

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
        if not isinstance(other, CheckpointExtraInfoResp):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
