# coding: utf-8

import pprint
import re

import six





class RealTimeConfInfo:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'chair_id': 'str'
    }

    attribute_map = {
        'chair_id': 'chairID'
    }

    def __init__(self, chair_id=None):
        """RealTimeConfInfo - a model defined in huaweicloud sdk"""
        
        

        self._chair_id = None
        self.discriminator = None

        if chair_id is not None:
            self.chair_id = chair_id

    @property
    def chair_id(self):
        """Gets the chair_id of this RealTimeConfInfo.

        主持人与会者标识。

        :return: The chair_id of this RealTimeConfInfo.
        :rtype: str
        """
        return self._chair_id

    @chair_id.setter
    def chair_id(self, chair_id):
        """Sets the chair_id of this RealTimeConfInfo.

        主持人与会者标识。

        :param chair_id: The chair_id of this RealTimeConfInfo.
        :type: str
        """
        self._chair_id = chair_id

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
        if not isinstance(other, RealTimeConfInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
