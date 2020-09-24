## Active learning workflow for Amazon Comprehend Custom Classification models with Amazon Augmented AI


## Deploying CloudFormation Template

We will start by deploying an AWS CloudFormation template to provision the necessary AWS Identity and Access Management (IAM) role and Lambda function needed in order to interact with the Amazon S3, AWS Lambda, and Amazon Comprehend APIs.
	Region	Region Code	Launch
1	US East 
(N. Virginia)	us-east-1

[![button](launchstack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?stackName=comprehend-active-learning&templateURL=https://aws-ml-blog.s3.amazonaws.com/artifacts/comprehend-a2i-active-learning/comprehend-active-learning-infra.yml)

#Architecture
-----------

Architecture below shows the core components. 

![](arch.png)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

