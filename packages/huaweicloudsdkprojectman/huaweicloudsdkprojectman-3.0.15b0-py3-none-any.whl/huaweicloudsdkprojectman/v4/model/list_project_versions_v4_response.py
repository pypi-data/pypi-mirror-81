# coding: utf-8

import pprint
import re

import six


from huaweicloudsdkcore.sdk_response import SdkResponse


class ListProjectVersionsV4Response(SdkResponse):


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'total': 'int',
        'iterations': 'list[ListProjectVersionsV4ResponseBodyIterations]'
    }

    attribute_map = {
        'total': 'total',
        'iterations': 'iterations'
    }

    def __init__(self, total=None, iterations=None):
        """ListProjectVersionsV4Response - a model defined in huaweicloud sdk"""
        
        super().__init__()

        self._total = None
        self._iterations = None
        self.discriminator = None

        if total is not None:
            self.total = total
        if iterations is not None:
            self.iterations = iterations

    @property
    def total(self):
        """Gets the total of this ListProjectVersionsV4Response.

        迭代总数

        :return: The total of this ListProjectVersionsV4Response.
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ListProjectVersionsV4Response.

        迭代总数

        :param total: The total of this ListProjectVersionsV4Response.
        :type: int
        """
        self._total = total

    @property
    def iterations(self):
        """Gets the iterations of this ListProjectVersionsV4Response.

        迭代信息

        :return: The iterations of this ListProjectVersionsV4Response.
        :rtype: list[ListProjectVersionsV4ResponseBodyIterations]
        """
        return self._iterations

    @iterations.setter
    def iterations(self, iterations):
        """Sets the iterations of this ListProjectVersionsV4Response.

        迭代信息

        :param iterations: The iterations of this ListProjectVersionsV4Response.
        :type: list[ListProjectVersionsV4ResponseBodyIterations]
        """
        self._iterations = iterations

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
        if not isinstance(other, ListProjectVersionsV4Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
