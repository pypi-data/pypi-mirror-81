# coding: utf-8

import pprint
import re

import six





class CheckpointReplicateRespbackups:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'backup_id': 'str',
        'replication_record_id': 'str'
    }

    attribute_map = {
        'backup_id': 'backup_id',
        'replication_record_id': 'replication_record_id'
    }

    def __init__(self, backup_id=None, replication_record_id=None):
        """CheckpointReplicateRespbackups - a model defined in huaweicloud sdk"""
        
        

        self._backup_id = None
        self._replication_record_id = None
        self.discriminator = None

        self.backup_id = backup_id
        self.replication_record_id = replication_record_id

    @property
    def backup_id(self):
        """Gets the backup_id of this CheckpointReplicateRespbackups.

        待复制的备份ID

        :return: The backup_id of this CheckpointReplicateRespbackups.
        :rtype: str
        """
        return self._backup_id

    @backup_id.setter
    def backup_id(self, backup_id):
        """Sets the backup_id of this CheckpointReplicateRespbackups.

        待复制的备份ID

        :param backup_id: The backup_id of this CheckpointReplicateRespbackups.
        :type: str
        """
        self._backup_id = backup_id

    @property
    def replication_record_id(self):
        """Gets the replication_record_id of this CheckpointReplicateRespbackups.

        复制记录ID

        :return: The replication_record_id of this CheckpointReplicateRespbackups.
        :rtype: str
        """
        return self._replication_record_id

    @replication_record_id.setter
    def replication_record_id(self, replication_record_id):
        """Sets the replication_record_id of this CheckpointReplicateRespbackups.

        复制记录ID

        :param replication_record_id: The replication_record_id of this CheckpointReplicateRespbackups.
        :type: str
        """
        self._replication_record_id = replication_record_id

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
        if not isinstance(other, CheckpointReplicateRespbackups):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
