# coding: utf-8

import pprint
import re

import six





class CreateCustomerV2Req:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'domain_name': 'str',
        'mobile_phone': 'str',
        'verification_code': 'str',
        'xaccount_id': 'str',
        'xaccount_type': 'str',
        'password': 'str',
        'is_close_market_ms': 'str',
        'cooperation_type': 'str',
        'indirect_partner_id': 'str'
    }

    attribute_map = {
        'domain_name': 'domain_name',
        'mobile_phone': 'mobile_phone',
        'verification_code': 'verification_code',
        'xaccount_id': 'xaccount_id',
        'xaccount_type': 'xaccount_type',
        'password': 'password',
        'is_close_market_ms': 'is_close_market_ms',
        'cooperation_type': 'cooperation_type',
        'indirect_partner_id': 'indirect_partner_id'
    }

    def __init__(self, domain_name=None, mobile_phone=None, verification_code=None, xaccount_id=None, xaccount_type=None, password=None, is_close_market_ms='false', cooperation_type=None, indirect_partner_id=None):
        """CreateCustomerV2Req - a model defined in huaweicloud sdk"""
        
        

        self._domain_name = None
        self._mobile_phone = None
        self._verification_code = None
        self._xaccount_id = None
        self._xaccount_type = None
        self._password = None
        self._is_close_market_ms = None
        self._cooperation_type = None
        self._indirect_partner_id = None
        self.discriminator = None

        if domain_name is not None:
            self.domain_name = domain_name
        if mobile_phone is not None:
            self.mobile_phone = mobile_phone
        if verification_code is not None:
            self.verification_code = verification_code
        self.xaccount_id = xaccount_id
        self.xaccount_type = xaccount_type
        if password is not None:
            self.password = password
        if is_close_market_ms is not None:
            self.is_close_market_ms = is_close_market_ms
        if cooperation_type is not None:
            self.cooperation_type = cooperation_type
        if indirect_partner_id is not None:
            self.indirect_partner_id = indirect_partner_id

    @property
    def domain_name(self):
        """Gets the domain_name of this CreateCustomerV2Req.

        |参数名称：客户的华为云账号名| |参数的约束及描述：该参数非必填，不能以“op_”或“shadow_”开头且不能全为数字。且只允许最大长度64的字符串,如果为空，随机生成。校验规则^[a-zA-Z0-9\\u00c0-\\u00ff-._ ]{0,64}$|

        :return: The domain_name of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._domain_name

    @domain_name.setter
    def domain_name(self, domain_name):
        """Sets the domain_name of this CreateCustomerV2Req.

        |参数名称：客户的华为云账号名| |参数的约束及描述：该参数非必填，不能以“op_”或“shadow_”开头且不能全为数字。且只允许最大长度64的字符串,如果为空，随机生成。校验规则^[a-zA-Z0-9\\u00c0-\\u00ff-._ ]{0,64}$|

        :param domain_name: The domain_name of this CreateCustomerV2Req.
        :type: str
        """
        self._domain_name = domain_name

    @property
    def mobile_phone(self):
        """Gets the mobile_phone of this CreateCustomerV2Req.

        |参数名称：手机号| |参数的约束及描述：如果接入的是华北站点，该字段必填，否则该字段忽略目前系统只支持中国手机，必须全部是数字。示例：13XXXXXXXXX|

        :return: The mobile_phone of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._mobile_phone

    @mobile_phone.setter
    def mobile_phone(self, mobile_phone):
        """Sets the mobile_phone of this CreateCustomerV2Req.

        |参数名称：手机号| |参数的约束及描述：如果接入的是华北站点，该字段必填，否则该字段忽略目前系统只支持中国手机，必须全部是数字。示例：13XXXXXXXXX|

        :param mobile_phone: The mobile_phone of this CreateCustomerV2Req.
        :type: str
        """
        self._mobile_phone = mobile_phone

    @property
    def verification_code(self):
        """Gets the verification_code of this CreateCustomerV2Req.

        |参数名称：验证码| |参数的约束及描述：该参数必填，如果输入的是手机，就是手机验证码，如果输入的是邮箱，就是邮箱验证码|

        :return: The verification_code of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._verification_code

    @verification_code.setter
    def verification_code(self, verification_code):
        """Sets the verification_code of this CreateCustomerV2Req.

        |参数名称：验证码| |参数的约束及描述：该参数必填，如果输入的是手机，就是手机验证码，如果输入的是邮箱，就是邮箱验证码|

        :param verification_code: The verification_code of this CreateCustomerV2Req.
        :type: str
        """
        self._verification_code = verification_code

    @property
    def xaccount_id(self):
        """Gets the xaccount_id of this CreateCustomerV2Req.

        |参数名称：第3方系统的用户唯一标识| |参数的约束及描述：该参数必填，且只允许最大长度128的字符串|

        :return: The xaccount_id of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._xaccount_id

    @xaccount_id.setter
    def xaccount_id(self, xaccount_id):
        """Sets the xaccount_id of this CreateCustomerV2Req.

        |参数名称：第3方系统的用户唯一标识| |参数的约束及描述：该参数必填，且只允许最大长度128的字符串|

        :param xaccount_id: The xaccount_id of this CreateCustomerV2Req.
        :type: str
        """
        self._xaccount_id = xaccount_id

    @property
    def xaccount_type(self):
        """Gets the xaccount_type of this CreateCustomerV2Req.

        |参数名称：华为分给合作伙伴的平台标识| |参数的约束及描述：该参数必填，且只允许最大长度30的字符串,该标识的具体值由华为分配|

        :return: The xaccount_type of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._xaccount_type

    @xaccount_type.setter
    def xaccount_type(self, xaccount_type):
        """Sets the xaccount_type of this CreateCustomerV2Req.

        |参数名称：华为分给合作伙伴的平台标识| |参数的约束及描述：该参数必填，且只允许最大长度30的字符串,该标识的具体值由华为分配|

        :param xaccount_type: The xaccount_type of this CreateCustomerV2Req.
        :type: str
        """
        self._xaccount_type = xaccount_type

    @property
    def password(self):
        """Gets the password of this CreateCustomerV2Req.

        |参数名称：密码| |参数的约束及描述：该参数选填，长度6~32位字符，至少包含以下四种字符中的两种： 大写字母、小写字母、数字、特殊字符，不能和账号名或倒序的账号名相同，不能包含手机号，不能包含邮箱|

        :return: The password of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this CreateCustomerV2Req.

        |参数名称：密码| |参数的约束及描述：该参数选填，长度6~32位字符，至少包含以下四种字符中的两种： 大写字母、小写字母、数字、特殊字符，不能和账号名或倒序的账号名相同，不能包含手机号，不能包含邮箱|

        :param password: The password of this CreateCustomerV2Req.
        :type: str
        """
        self._password = password

    @property
    def is_close_market_ms(self):
        """Gets the is_close_market_ms of this CreateCustomerV2Req.

        |是否关闭营销消息| |参数的约束及描述：该参数选填。false：不关闭，True：关闭，默认不关闭|

        :return: The is_close_market_ms of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._is_close_market_ms

    @is_close_market_ms.setter
    def is_close_market_ms(self, is_close_market_ms):
        """Sets the is_close_market_ms of this CreateCustomerV2Req.

        |是否关闭营销消息| |参数的约束及描述：该参数选填。false：不关闭，True：关闭，默认不关闭|

        :param is_close_market_ms: The is_close_market_ms of this CreateCustomerV2Req.
        :type: str
        """
        self._is_close_market_ms = is_close_market_ms

    @property
    def cooperation_type(self):
        """Gets the cooperation_type of this CreateCustomerV2Req.

        |合作类型| |参数的约束及描述：该参数选填。1：推荐。仅仅支持1|

        :return: The cooperation_type of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._cooperation_type

    @cooperation_type.setter
    def cooperation_type(self, cooperation_type):
        """Sets the cooperation_type of this CreateCustomerV2Req.

        |合作类型| |参数的约束及描述：该参数选填。1：推荐。仅仅支持1|

        :param cooperation_type: The cooperation_type of this CreateCustomerV2Req.
        :type: str
        """
        self._cooperation_type = cooperation_type

    @property
    def indirect_partner_id(self):
        """Gets the indirect_partner_id of this CreateCustomerV2Req.

        |参数名称：二级渠道ID| |参数的约束及描述：该参数非必填，二级渠道ID，最大长度64|

        :return: The indirect_partner_id of this CreateCustomerV2Req.
        :rtype: str
        """
        return self._indirect_partner_id

    @indirect_partner_id.setter
    def indirect_partner_id(self, indirect_partner_id):
        """Sets the indirect_partner_id of this CreateCustomerV2Req.

        |参数名称：二级渠道ID| |参数的约束及描述：该参数非必填，二级渠道ID，最大长度64|

        :param indirect_partner_id: The indirect_partner_id of this CreateCustomerV2Req.
        :type: str
        """
        self._indirect_partner_id = indirect_partner_id

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
        if not isinstance(other, CreateCustomerV2Req):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
