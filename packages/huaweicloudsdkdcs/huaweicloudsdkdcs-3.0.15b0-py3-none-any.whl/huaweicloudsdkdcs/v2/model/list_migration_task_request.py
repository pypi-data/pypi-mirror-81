# coding: utf-8

import pprint
import re

import six





class ListMigrationTaskRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'offset': 'int',
        'limit': 'int',
        'name': 'str'
    }

    attribute_map = {
        'offset': 'offset',
        'limit': 'limit',
        'name': 'name'
    }

    def __init__(self, offset=None, limit=None, name=None):
        """ListMigrationTaskRequest - a model defined in huaweicloud sdk"""
        
        

        self._offset = None
        self._limit = None
        self._name = None
        self.discriminator = None

        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit
        if name is not None:
            self.name = name

    @property
    def offset(self):
        """Gets the offset of this ListMigrationTaskRequest.


        :return: The offset of this ListMigrationTaskRequest.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ListMigrationTaskRequest.


        :param offset: The offset of this ListMigrationTaskRequest.
        :type: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this ListMigrationTaskRequest.


        :return: The limit of this ListMigrationTaskRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListMigrationTaskRequest.


        :param limit: The limit of this ListMigrationTaskRequest.
        :type: int
        """
        self._limit = limit

    @property
    def name(self):
        """Gets the name of this ListMigrationTaskRequest.


        :return: The name of this ListMigrationTaskRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ListMigrationTaskRequest.


        :param name: The name of this ListMigrationTaskRequest.
        :type: str
        """
        self._name = name

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
        if not isinstance(other, ListMigrationTaskRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
