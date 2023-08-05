# coding: utf-8

import pprint
import re

import six





class MetricInfoExt:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'dimensions': 'list[MetricsDimension]',
        'metric_name': 'str',
        'namespace': 'str'
    }

    attribute_map = {
        'dimensions': 'dimensions',
        'metric_name': 'metric_name',
        'namespace': 'namespace'
    }

    def __init__(self, dimensions=None, metric_name=None, namespace=None):
        """MetricInfoExt - a model defined in huaweicloud sdk"""
        
        

        self._dimensions = None
        self._metric_name = None
        self._namespace = None
        self.discriminator = None

        self.dimensions = dimensions
        self.metric_name = metric_name
        self.namespace = namespace

    @property
    def dimensions(self):
        """Gets the dimensions of this MetricInfoExt.

        指标维度

        :return: The dimensions of this MetricInfoExt.
        :rtype: list[MetricsDimension]
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """Sets the dimensions of this MetricInfoExt.

        指标维度

        :param dimensions: The dimensions of this MetricInfoExt.
        :type: list[MetricsDimension]
        """
        self._dimensions = dimensions

    @property
    def metric_name(self):
        """Gets the metric_name of this MetricInfoExt.

        指标名称，必须以字母开头，只能包含0-9/a-z/A-Z/_，长度最短为1，最大为64。  具体指标名请参见查询指标列表中查询出的指标名。

        :return: The metric_name of this MetricInfoExt.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """Sets the metric_name of this MetricInfoExt.

        指标名称，必须以字母开头，只能包含0-9/a-z/A-Z/_，长度最短为1，最大为64。  具体指标名请参见查询指标列表中查询出的指标名。

        :param metric_name: The metric_name of this MetricInfoExt.
        :type: str
        """
        self._metric_name = metric_name

    @property
    def namespace(self):
        """Gets the namespace of this MetricInfoExt.

        指标命名空间，，例如弹性云服务器命名空间。格式为service.item；service和item必须是字符串，必须以字母开头，只能包含0-9/a-z/A-Z/_，总长度最短为3，最大为32。说明： 当alarm_type为（EVENT.SYS| EVENT.CUSTOM）时允许为空。

        :return: The namespace of this MetricInfoExt.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this MetricInfoExt.

        指标命名空间，，例如弹性云服务器命名空间。格式为service.item；service和item必须是字符串，必须以字母开头，只能包含0-9/a-z/A-Z/_，总长度最短为3，最大为32。说明： 当alarm_type为（EVENT.SYS| EVENT.CUSTOM）时允许为空。

        :param namespace: The namespace of this MetricInfoExt.
        :type: str
        """
        self._namespace = namespace

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
        if not isinstance(other, MetricInfoExt):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
