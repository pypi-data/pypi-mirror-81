# AWS Session Management

This package contains 

AwsSessionManagement - handles AWS Session with AWS Temp credentials by Assuming a given Role
                       it renews the temp credentials when needed
This library helps keeping boto3 clients with the fresh aws temp credentials

Usage:

This example shows how to manage the AWSRequestAuth object with the fresh temp credentials 
These credentials will be automatically refreshed by the AwsSessionManamagement class

Using the following libraries:

import requests
import aws_requests_auth (https://github.com/DavidMuller/aws-requests-auth)

```


def get_auth_request(aws_access_key_id, aws_secret_access_key, aws_session_token, aws_host, aws_region, aws_service):
    logger.info("creating/updating auth request ...")
    auth = AWSRequestsAuth(aws_access_key=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key,
                           aws_token=aws_session_token,
                           aws_host=aws_host,
                           aws_region=aws_region,
                           aws_service=aws_service)
    logger.info("returning auth request")
    return auth



awsSessionManagement = AwsSessionManagement(role_arn='roleArnValue',
                                            external_id='externalIdValue',
                                            func=get_auth_request,
                                            func_params_dict={'aws_host': 'your_service_aws_host_name', 'aws_region': 'your_service_region', 'aws_service': 'your_aws_service_name'},
                                            role_session_name="CurrentSession")

# For example:
# aws_host = f'{self.api_gateway_id}.execute-api.{self.api_gateway_region}.amazonaws.com'
# aws_region = 'eu-west-1'
# aws_service = 'execute-api'

# get the auth request object with the temp aws credentials
auth = awsSessionManagement.get_func_res()
headers = {'Accept': 'application/json'}
response = requests.get(f"{self.api_gateway_url}/abc", auth=auth, headers=headers)


```
 