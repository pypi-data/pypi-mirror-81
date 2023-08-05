# coding: utf-8

import pprint
import re

import six


from huaweicloudsdkcore.sdk_response import SdkResponse


class CreatePlanResponse(SdkResponse):


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'plan_id': 'str',
        'error_code': 'str',
        'error_msg': 'str'
    }

    attribute_map = {
        'plan_id': 'plan_id',
        'error_code': 'error_code',
        'error_msg': 'error_msg'
    }

    def __init__(self, plan_id=None, error_code=None, error_msg=None):
        """CreatePlanResponse - a model defined in huaweicloud sdk"""
        
        super().__init__()

        self._plan_id = None
        self._error_code = None
        self._error_msg = None
        self.discriminator = None

        if plan_id is not None:
            self.plan_id = plan_id
        if error_code is not None:
            self.error_code = error_code
        if error_msg is not None:
            self.error_msg = error_msg

    @property
    def plan_id(self):
        """Gets the plan_id of this CreatePlanResponse.

        接口调用成功返回的计划id

        :return: The plan_id of this CreatePlanResponse.
        :rtype: str
        """
        return self._plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        """Sets the plan_id of this CreatePlanResponse.

        接口调用成功返回的计划id

        :param plan_id: The plan_id of this CreatePlanResponse.
        :type: str
        """
        self._plan_id = plan_id

    @property
    def error_code(self):
        """Gets the error_code of this CreatePlanResponse.

        接口调用成功不返回，调用失败错误码

        :return: The error_code of this CreatePlanResponse.
        :rtype: str
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code):
        """Sets the error_code of this CreatePlanResponse.

        接口调用成功不返回，调用失败错误码

        :param error_code: The error_code of this CreatePlanResponse.
        :type: str
        """
        self._error_code = error_code

    @property
    def error_msg(self):
        """Gets the error_msg of this CreatePlanResponse.

        接口调用成功不返回，调用失败错误信息

        :return: The error_msg of this CreatePlanResponse.
        :rtype: str
        """
        return self._error_msg

    @error_msg.setter
    def error_msg(self, error_msg):
        """Sets the error_msg of this CreatePlanResponse.

        接口调用成功不返回，调用失败错误信息

        :param error_msg: The error_msg of this CreatePlanResponse.
        :type: str
        """
        self._error_msg = error_msg

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
        if not isinstance(other, CreatePlanResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
