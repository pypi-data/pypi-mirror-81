# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.models.inline_response20013 import InlineResponse20013  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException

class TestInlineResponse20013(unittest.TestCase):
    """InlineResponse20013 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse20013
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulpcore.models.inline_response20013.InlineResponse20013()  # noqa: E501
        if include_optional :
            return InlineResponse20013(
                count = 123, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulpcore.models.user_response.UserResponse(
                        pulp_href = '0', 
                        id = 56, 
                        username = '0', 
                        first_name = '0', 
                        last_name = '0', 
                        email = '0', 
                        is_staff = True, 
                        is_active = True, 
                        date_joined = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        groups = [
                            pulpcore.client.pulpcore.models.user_group_response.UserGroupResponse(
                                name = '0', 
                                pulp_href = '0', )
                            ], )
                    ]
            )
        else :
            return InlineResponse20013(
        )

    def testInlineResponse20013(self):
        """Test InlineResponse20013"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
