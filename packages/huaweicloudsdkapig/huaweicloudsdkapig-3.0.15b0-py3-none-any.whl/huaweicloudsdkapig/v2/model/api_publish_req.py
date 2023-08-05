# coding: utf-8

import pprint
import re

import six





class ApiPublishReq:


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
        'env_id': 'str',
        'api_id': 'str',
        'remark': 'str'
    }

    attribute_map = {
        'action': 'action',
        'env_id': 'env_id',
        'api_id': 'api_id',
        'remark': 'remark'
    }

    def __init__(self, action=None, env_id=None, api_id=None, remark=None):
        """ApiPublishReq - a model defined in huaweicloud sdk"""
        
        

        self._action = None
        self._env_id = None
        self._api_id = None
        self._remark = None
        self.discriminator = None

        self.action = action
        self.env_id = env_id
        self.api_id = api_id
        if remark is not None:
            self.remark = remark

    @property
    def action(self):
        """Gets the action of this ApiPublishReq.

        需要进行的操作。 - online：发布 - offline：下线

        :return: The action of this ApiPublishReq.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this ApiPublishReq.

        需要进行的操作。 - online：发布 - offline：下线

        :param action: The action of this ApiPublishReq.
        :type: str
        """
        self._action = action

    @property
    def env_id(self):
        """Gets the env_id of this ApiPublishReq.

        环境的编号，即：API需要发布到哪个环境

        :return: The env_id of this ApiPublishReq.
        :rtype: str
        """
        return self._env_id

    @env_id.setter
    def env_id(self, env_id):
        """Sets the env_id of this ApiPublishReq.

        环境的编号，即：API需要发布到哪个环境

        :param env_id: The env_id of this ApiPublishReq.
        :type: str
        """
        self._env_id = env_id

    @property
    def api_id(self):
        """Gets the api_id of this ApiPublishReq.

        API的编号，即：需要进行发布或下线的API的编号

        :return: The api_id of this ApiPublishReq.
        :rtype: str
        """
        return self._api_id

    @api_id.setter
    def api_id(self, api_id):
        """Sets the api_id of this ApiPublishReq.

        API的编号，即：需要进行发布或下线的API的编号

        :param api_id: The api_id of this ApiPublishReq.
        :type: str
        """
        self._api_id = api_id

    @property
    def remark(self):
        """Gets the remark of this ApiPublishReq.

        对发布动作的简述。字符长度不超过255 > 中文字符必须为UTF-8或者unicode编码。

        :return: The remark of this ApiPublishReq.
        :rtype: str
        """
        return self._remark

    @remark.setter
    def remark(self, remark):
        """Sets the remark of this ApiPublishReq.

        对发布动作的简述。字符长度不超过255 > 中文字符必须为UTF-8或者unicode编码。

        :param remark: The remark of this ApiPublishReq.
        :type: str
        """
        self._remark = remark

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
        if not isinstance(other, ApiPublishReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
