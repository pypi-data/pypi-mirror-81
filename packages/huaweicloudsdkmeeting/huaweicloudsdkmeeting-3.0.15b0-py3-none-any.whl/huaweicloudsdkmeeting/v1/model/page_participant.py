# coding: utf-8

import pprint
import re

import six





class PageParticipant:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'data': 'list[ParticipantInfo]',
        'offset': 'int',
        'limit': 'int',
        'count': 'int'
    }

    attribute_map = {
        'data': 'data',
        'offset': 'offset',
        'limit': 'limit',
        'count': 'count'
    }

    def __init__(self, data=None, offset=None, limit=None, count=None):
        """PageParticipant - a model defined in huaweicloud sdk"""
        
        

        self._data = None
        self._offset = None
        self._limit = None
        self._count = None
        self.discriminator = None

        if data is not None:
            self.data = data
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit
        if count is not None:
            self.count = count

    @property
    def data(self):
        """Gets the data of this PageParticipant.

        与会者信息。

        :return: The data of this PageParticipant.
        :rtype: list[ParticipantInfo]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this PageParticipant.

        与会者信息。

        :param data: The data of this PageParticipant.
        :type: list[ParticipantInfo]
        """
        self._data = data

    @property
    def offset(self):
        """Gets the offset of this PageParticipant.

        记录数偏移，这一页之前共有多少条。

        :return: The offset of this PageParticipant.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this PageParticipant.

        记录数偏移，这一页之前共有多少条。

        :param offset: The offset of this PageParticipant.
        :type: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this PageParticipant.

        每页的记录数。

        :return: The limit of this PageParticipant.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this PageParticipant.

        每页的记录数。

        :param limit: The limit of this PageParticipant.
        :type: int
        """
        self._limit = limit

    @property
    def count(self):
        """Gets the count of this PageParticipant.

        总记录数。

        :return: The count of this PageParticipant.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this PageParticipant.

        总记录数。

        :param count: The count of this PageParticipant.
        :type: int
        """
        self._count = count

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
        if not isinstance(other, PageParticipant):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
