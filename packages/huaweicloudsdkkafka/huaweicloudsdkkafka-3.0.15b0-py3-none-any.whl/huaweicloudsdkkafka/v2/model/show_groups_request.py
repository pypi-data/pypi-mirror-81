# coding: utf-8

import pprint
import re

import six





class ShowGroupsRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'instance_id': 'str',
        'group': 'str'
    }

    attribute_map = {
        'instance_id': 'instance_id',
        'group': 'group'
    }

    def __init__(self, instance_id=None, group=None):
        """ShowGroupsRequest - a model defined in huaweicloud sdk"""
        
        

        self._instance_id = None
        self._group = None
        self.discriminator = None

        self.instance_id = instance_id
        self.group = group

    @property
    def instance_id(self):
        """Gets the instance_id of this ShowGroupsRequest.


        :return: The instance_id of this ShowGroupsRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ShowGroupsRequest.


        :param instance_id: The instance_id of this ShowGroupsRequest.
        :type: str
        """
        self._instance_id = instance_id

    @property
    def group(self):
        """Gets the group of this ShowGroupsRequest.


        :return: The group of this ShowGroupsRequest.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this ShowGroupsRequest.


        :param group: The group of this ShowGroupsRequest.
        :type: str
        """
        self._group = group

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
        if not isinstance(other, ShowGroupsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
