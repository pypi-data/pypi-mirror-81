# coding: utf-8

import pprint
import re

import six





class BlackEnhance:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'early_report': 'str',
        'position': 'str',
        'start_time': 'str'
    }

    attribute_map = {
        'early_report': 'early_report',
        'position': 'position',
        'start_time': 'start_time'
    }

    def __init__(self, early_report=None, position=None, start_time=None):
        """BlackEnhance - a model defined in huaweicloud sdk"""
        
        

        self._early_report = None
        self._position = None
        self._start_time = None
        self.discriminator = None

        if early_report is not None:
            self.early_report = early_report
        if position is not None:
            self.position = position
        if start_time is not None:
            self.start_time = start_time

    @property
    def early_report(self):
        """Gets the early_report of this BlackEnhance.

        提前反馈“疑似黑边”开关，取值为on或off。 

        :return: The early_report of this BlackEnhance.
        :rtype: str
        """
        return self._early_report

    @early_report.setter
    def early_report(self, early_report):
        """Sets the early_report of this BlackEnhance.

        提前反馈“疑似黑边”开关，取值为on或off。 

        :param early_report: The early_report of this BlackEnhance.
        :type: str
        """
        self._early_report = early_report

    @property
    def position(self):
        """Gets the position of this BlackEnhance.

        参数格式：top:bottom:left:right 

        :return: The position of this BlackEnhance.
        :rtype: str
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this BlackEnhance.

        参数格式：top:bottom:left:right 

        :param position: The position of this BlackEnhance.
        :type: str
        """
        self._position = position

    @property
    def start_time(self):
        """Gets the start_time of this BlackEnhance.

        黑边剪裁检测起始时间 

        :return: The start_time of this BlackEnhance.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this BlackEnhance.

        黑边剪裁检测起始时间 

        :param start_time: The start_time of this BlackEnhance.
        :type: str
        """
        self._start_time = start_time

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
        if not isinstance(other, BlackEnhance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
