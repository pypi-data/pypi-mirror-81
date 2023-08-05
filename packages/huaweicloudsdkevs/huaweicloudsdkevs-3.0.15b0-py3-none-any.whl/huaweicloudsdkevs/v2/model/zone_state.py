# coding: utf-8

import pprint
import re

import six





class ZoneState:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'available': 'bool'
    }

    attribute_map = {
        'available': 'available'
    }

    def __init__(self, available=None):
        """ZoneState - a model defined in huaweicloud sdk"""
        
        

        self._available = None
        self.discriminator = None

        if available is not None:
            self.available = available

    @property
    def available(self):
        """Gets the available of this ZoneState.

        可用分区是否可用。

        :return: The available of this ZoneState.
        :rtype: bool
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this ZoneState.

        可用分区是否可用。

        :param available: The available of this ZoneState.
        :type: bool
        """
        self._available = available

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
        if not isinstance(other, ZoneState):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
