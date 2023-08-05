# coding: utf-8

import pprint
import re

import six





class UpdateTestCaseRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'name': 'str',
        'service_id': 'int',
        'rank_id': 'str',
        'testcase_number': 'str',
        'extend_info': 'ExternalServiceBizCase'
    }

    attribute_map = {
        'name': 'name',
        'service_id': 'service_id',
        'rank_id': 'rank_id',
        'testcase_number': 'testcase_number',
        'extend_info': 'extend_info'
    }

    def __init__(self, name=None, service_id=None, rank_id=None, testcase_number=None, extend_info=None):
        """UpdateTestCaseRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._name = None
        self._service_id = None
        self._rank_id = None
        self._testcase_number = None
        self._extend_info = None
        self.discriminator = None

        self.name = name
        self.service_id = service_id
        if rank_id is not None:
            self.rank_id = rank_id
        if testcase_number is not None:
            self.testcase_number = testcase_number
        if extend_info is not None:
            self.extend_info = extend_info

    @property
    def name(self):
        """Gets the name of this UpdateTestCaseRequestBody.

        云测页面上显示的用例名称，长度为[3-128]位字符

        :return: The name of this UpdateTestCaseRequestBody.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateTestCaseRequestBody.

        云测页面上显示的用例名称，长度为[3-128]位字符

        :param name: The name of this UpdateTestCaseRequestBody.
        :type: str
        """
        self._name = name

    @property
    def service_id(self):
        """Gets the service_id of this UpdateTestCaseRequestBody.

        注册结果返回的服务id

        :return: The service_id of this UpdateTestCaseRequestBody.
        :rtype: int
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        """Sets the service_id of this UpdateTestCaseRequestBody.

        注册结果返回的服务id

        :param service_id: The service_id of this UpdateTestCaseRequestBody.
        :type: int
        """
        self._service_id = service_id

    @property
    def rank_id(self):
        """Gets the rank_id of this UpdateTestCaseRequestBody.

        测试用例等级，可选值为[0,1,2,3,4]，不填时云测默认为2

        :return: The rank_id of this UpdateTestCaseRequestBody.
        :rtype: str
        """
        return self._rank_id

    @rank_id.setter
    def rank_id(self, rank_id):
        """Sets the rank_id of this UpdateTestCaseRequestBody.

        测试用例等级，可选值为[0,1,2,3,4]，不填时云测默认为2

        :param rank_id: The rank_id of this UpdateTestCaseRequestBody.
        :type: str
        """
        self._rank_id = rank_id

    @property
    def testcase_number(self):
        """Gets the testcase_number of this UpdateTestCaseRequestBody.

        用例编号，不填该值时云测会自动生成，长度为[3-128]位字符

        :return: The testcase_number of this UpdateTestCaseRequestBody.
        :rtype: str
        """
        return self._testcase_number

    @testcase_number.setter
    def testcase_number(self, testcase_number):
        """Sets the testcase_number of this UpdateTestCaseRequestBody.

        用例编号，不填该值时云测会自动生成，长度为[3-128]位字符

        :param testcase_number: The testcase_number of this UpdateTestCaseRequestBody.
        :type: str
        """
        self._testcase_number = testcase_number

    @property
    def extend_info(self):
        """Gets the extend_info of this UpdateTestCaseRequestBody.


        :return: The extend_info of this UpdateTestCaseRequestBody.
        :rtype: ExternalServiceBizCase
        """
        return self._extend_info

    @extend_info.setter
    def extend_info(self, extend_info):
        """Sets the extend_info of this UpdateTestCaseRequestBody.


        :param extend_info: The extend_info of this UpdateTestCaseRequestBody.
        :type: ExternalServiceBizCase
        """
        self._extend_info = extend_info

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
        if not isinstance(other, UpdateTestCaseRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
