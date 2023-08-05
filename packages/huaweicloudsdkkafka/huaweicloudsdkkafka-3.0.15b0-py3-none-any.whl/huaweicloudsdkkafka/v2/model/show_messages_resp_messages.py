# coding: utf-8

import pprint
import re

import six





class ShowMessagesRespMessages:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'topic': 'str',
        'partition': 'int',
        'message_offset': 'int',
        'size': 'int'
    }

    attribute_map = {
        'topic': 'topic',
        'partition': 'partition',
        'message_offset': 'message_offset',
        'size': 'size'
    }

    def __init__(self, topic=None, partition=None, message_offset=None, size=None):
        """ShowMessagesRespMessages - a model defined in huaweicloud sdk"""
        
        

        self._topic = None
        self._partition = None
        self._message_offset = None
        self._size = None
        self.discriminator = None

        if topic is not None:
            self.topic = topic
        if partition is not None:
            self.partition = partition
        if message_offset is not None:
            self.message_offset = message_offset
        if size is not None:
            self.size = size

    @property
    def topic(self):
        """Gets the topic of this ShowMessagesRespMessages.

        topic名称。

        :return: The topic of this ShowMessagesRespMessages.
        :rtype: str
        """
        return self._topic

    @topic.setter
    def topic(self, topic):
        """Sets the topic of this ShowMessagesRespMessages.

        topic名称。

        :param topic: The topic of this ShowMessagesRespMessages.
        :type: str
        """
        self._topic = topic

    @property
    def partition(self):
        """Gets the partition of this ShowMessagesRespMessages.

        分区编号。

        :return: The partition of this ShowMessagesRespMessages.
        :rtype: int
        """
        return self._partition

    @partition.setter
    def partition(self, partition):
        """Sets the partition of this ShowMessagesRespMessages.

        分区编号。

        :param partition: The partition of this ShowMessagesRespMessages.
        :type: int
        """
        self._partition = partition

    @property
    def message_offset(self):
        """Gets the message_offset of this ShowMessagesRespMessages.

        消息编号。

        :return: The message_offset of this ShowMessagesRespMessages.
        :rtype: int
        """
        return self._message_offset

    @message_offset.setter
    def message_offset(self, message_offset):
        """Sets the message_offset of this ShowMessagesRespMessages.

        消息编号。

        :param message_offset: The message_offset of this ShowMessagesRespMessages.
        :type: int
        """
        self._message_offset = message_offset

    @property
    def size(self):
        """Gets the size of this ShowMessagesRespMessages.

        消息大小，单位字节。

        :return: The size of this ShowMessagesRespMessages.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ShowMessagesRespMessages.

        消息大小，单位字节。

        :param size: The size of this ShowMessagesRespMessages.
        :type: int
        """
        self._size = size

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
        if not isinstance(other, ShowMessagesRespMessages):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
