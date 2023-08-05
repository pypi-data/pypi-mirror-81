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

def get_auth(self):
    auth = None

    if self.awsSessionManagement is not None:
        aws_access_key_id, aws_secret_access_key, aws_session_token = self.awsSessionManagement.get_aws_credentials()
        if aws_access_key_id is not None and aws_secret_access_key is not None and aws_session_token is not None:
            logger.debug("got aws credentials, using for authentication")
            auth = AWSRequestsAuth(aws_access_key=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   aws_token=aws_session_token,
                                   aws_host=f'{self.wmc_api_id}.execute-api.{self.wmc_api_region}.amazonaws.com',
                                   aws_region=self.wmc_api_region,
                                   aws_service='execute-api')
        else:
            logger.warning("ALL the retrieved aws credentials are None, not using authentication!")

    return auth


headers = {'content-type': 'application/json'}
json_data = {"a": 'a_value', "b": 'b_value'}
data = json.dumps(json_data)
response = requests.post(url=f"{self.api_gateway}/abc", auth=self.get_auth(), data=data, headers=headers)

```

OR Alternatively you can use AwsSessionManagement as follows:

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


 