# coding: utf-8

import pprint
import re

import six





class ListScalingPolicyExecuteLogsRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'scaling_policy_id': 'str',
        'log_id': 'str',
        'scaling_resource_type': 'str',
        'scaling_resource_id': 'str',
        'execute_type': 'str',
        'start_time': 'datetime',
        'end_time': 'datetime',
        'start_number': 'int',
        'limit': 'int'
    }

    attribute_map = {
        'scaling_policy_id': 'scaling_policy_id',
        'log_id': 'log_id',
        'scaling_resource_type': 'scaling_resource_type',
        'scaling_resource_id': 'scaling_resource_id',
        'execute_type': 'execute_type',
        'start_time': 'start_time',
        'end_time': 'end_time',
        'start_number': 'start_number',
        'limit': 'limit'
    }

    def __init__(self, scaling_policy_id=None, log_id=None, scaling_resource_type=None, scaling_resource_id=None, execute_type=None, start_time=None, end_time=None, start_number=None, limit=None):
        """ListScalingPolicyExecuteLogsRequest - a model defined in huaweicloud sdk"""
        
        

        self._scaling_policy_id = None
        self._log_id = None
        self._scaling_resource_type = None
        self._scaling_resource_id = None
        self._execute_type = None
        self._start_time = None
        self._end_time = None
        self._start_number = None
        self._limit = None
        self.discriminator = None

        self.scaling_policy_id = scaling_policy_id
        if log_id is not None:
            self.log_id = log_id
        if scaling_resource_type is not None:
            self.scaling_resource_type = scaling_resource_type
        if scaling_resource_id is not None:
            self.scaling_resource_id = scaling_resource_id
        if execute_type is not None:
            self.execute_type = execute_type
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if start_number is not None:
            self.start_number = start_number
        if limit is not None:
            self.limit = limit

    @property
    def scaling_policy_id(self):
        """Gets the scaling_policy_id of this ListScalingPolicyExecuteLogsRequest.


        :return: The scaling_policy_id of this ListScalingPolicyExecuteLogsRequest.
        :rtype: str
        """
        return self._scaling_policy_id

    @scaling_policy_id.setter
    def scaling_policy_id(self, scaling_policy_id):
        """Sets the scaling_policy_id of this ListScalingPolicyExecuteLogsRequest.


        :param scaling_policy_id: The scaling_policy_id of this ListScalingPolicyExecuteLogsRequest.
        :type: str
        """
        self._scaling_policy_id = scaling_policy_id

    @property
    def log_id(self):
        """Gets the log_id of this ListScalingPolicyExecuteLogsRequest.


        :return: The log_id of this ListScalingPolicyExecuteLogsRequest.
        :rtype: str
        """
        return self._log_id

    @log_id.setter
    def log_id(self, log_id):
        """Sets the log_id of this ListScalingPolicyExecuteLogsRequest.


        :param log_id: The log_id of this ListScalingPolicyExecuteLogsRequest.
        :type: str
        """
        self._log_id = log_id

    @property
    def scaling_resource_type(self):
        """Gets the scaling_resource_type of this ListScalingPolicyExecuteLogsRequest.


        :return: The scaling_resource_type of this ListScalingPolicyExecuteLogsRequest.
        :rtype: str
        """
        return self._scaling_resource_type

    @scaling_resource_type.setter
    def scaling_resource_type(self, scaling_resource_type):
        """Sets the scaling_resource_type of this ListScalingPolicyExecuteLogsRequest.


        :param scaling_resource_type: The scaling_resource_type of this ListScalingPolicyExecuteLogsRequest.
        :type: str
        """
        self._scaling_resource_type = scaling_resource_type

    @property
    def scaling_resource_id(self):
        """Gets the scaling_resource_id of this ListScalingPolicyExecuteLogsRequest.


        :return: The scaling_resource_id of this ListScalingPolicyExecuteLogsRequest.
        :rtype: str
        """
        return self._scaling_resource_id

    @scaling_resource_id.setter
    def scaling_resource_id(self, scaling_resource_id):
        """Sets the scaling_resource_id of this ListScalingPolicyExecuteLogsRequest.


        :param scaling_resource_id: The scaling_resource_id of this ListScalingPolicyExecuteLogsRequest.
        :type: str
        """
        self._scaling_resource_id = scaling_resource_id

    @property
    def execute_type(self):
        """Gets the execute_type of this ListScalingPolicyExecuteLogsRequest.


        :return: The execute_type of this ListScalingPolicyExecuteLogsRequest.
        :rtype: str
        """
        return self._execute_type

    @execute_type.setter
    def execute_type(self, execute_type):
        """Sets the execute_type of this ListScalingPolicyExecuteLogsRequest.


        :param execute_type: The execute_type of this ListScalingPolicyExecuteLogsRequest.
        :type: str
        """
        self._execute_type = execute_type

    @property
    def start_time(self):
        """Gets the start_time of this ListScalingPolicyExecuteLogsRequest.


        :return: The start_time of this ListScalingPolicyExecuteLogsRequest.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this ListScalingPolicyExecuteLogsRequest.


        :param start_time: The start_time of this ListScalingPolicyExecuteLogsRequest.
        :type: datetime
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this ListScalingPolicyExecuteLogsRequest.


        :return: The end_time of this ListScalingPolicyExecuteLogsRequest.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this ListScalingPolicyExecuteLogsRequest.


        :param end_time: The end_time of this ListScalingPolicyExecuteLogsRequest.
        :type: datetime
        """
        self._end_time = end_time

    @property
    def start_number(self):
        """Gets the start_number of this ListScalingPolicyExecuteLogsRequest.


        :return: The start_number of this ListScalingPolicyExecuteLogsRequest.
        :rtype: int
        """
        return self._start_number

    @start_number.setter
    def start_number(self, start_number):
        """Sets the start_number of this ListScalingPolicyExecuteLogsRequest.


        :param start_number: The start_number of this ListScalingPolicyExecuteLogsRequest.
        :type: int
        """
        self._start_number = start_number

    @property
    def limit(self):
        """Gets the limit of this ListScalingPolicyExecuteLogsRequest.


        :return: The limit of this ListScalingPolicyExecuteLogsRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListScalingPolicyExecuteLogsRequest.


        :param limit: The limit of this ListScalingPolicyExecuteLogsRequest.
        :type: int
        """
        self._limit = limit

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
        if not isinstance(other, ListScalingPolicyExecuteLogsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
