# coding: utf-8

import pprint
import re

import six





class BatchDeleteVolumeTagsRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'action': 'str',
        'tags': 'list[DeleteTagsOption]'
    }

    attribute_map = {
        'action': 'action',
        'tags': 'tags'
    }

    def __init__(self, action='delete', tags=None):
        """BatchDeleteVolumeTagsRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._action = None
        self._tags = None
        self.discriminator = None

        self.action = action
        self.tags = tags

    @property
    def action(self):
        """Gets the action of this BatchDeleteVolumeTagsRequestBody.

        操作标识，当前支持的取值如下：  删除标签：delete

        :return: The action of this BatchDeleteVolumeTagsRequestBody.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this BatchDeleteVolumeTagsRequestBody.

        操作标识，当前支持的取值如下：  删除标签：delete

        :param action: The action of this BatchDeleteVolumeTagsRequestBody.
        :type: str
        """
        self._action = action

    @property
    def tags(self):
        """Gets the tags of this BatchDeleteVolumeTagsRequestBody.

        标签列表。

        :return: The tags of this BatchDeleteVolumeTagsRequestBody.
        :rtype: list[DeleteTagsOption]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this BatchDeleteVolumeTagsRequestBody.

        标签列表。

        :param tags: The tags of this BatchDeleteVolumeTagsRequestBody.
        :type: list[DeleteTagsOption]
        """
        self._tags = tags

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
        if not isinstance(other, BatchDeleteVolumeTagsRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
