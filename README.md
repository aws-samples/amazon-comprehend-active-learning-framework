## Active learning workflow for Amazon Comprehend Custom Classification models with Amazon Augmented AI
Amazon Comprehend  Custom Classification API enables you to easily build custom text classification models using your business-specific labels without learning ML. For example, your customer support organization can use Custom Classification to automatically categorize inbound requests by problem type based on how the customer has described the issue.  You can use custom classifiers to automatically label support emails with appropriate issue types, routing customer phone calls to the right agents, and categorizing social media posts into user segments.

For custom classification, you start by creating a training job with a ground truth dataset comprising a collection of text and corresponding category labels. Upon completing the job, you have a classifier that can classify any new text into one or more named categories. When the custom classification model classifies a new unlabeled text document, it predicts what it has learned from the training data. Sometimes you may not have a training dataset with various language patterns, or once you deploy the model, you start seeing completely new data patterns. In these cases, the model may not be able to classify these new data patterns accurately. How can we ensure continuous model training to keep it up to date with new data and patterns?



## Feedback Workflow Architecture.


The following diagram illustrates the architecture of the solution

![](arch.png)

In this section, we discuss an architectural pattern for implementing an end-to-end active learning workflow for custom classification models in Amazon Comprehend using Amazon A2I. The active learning workflow comprises the following components:

Real-time classification
Feedback loops
Human classification
Model building
Model selection
Model deployment
The following diagram illustrates this architecture covering the first three components. In the following sections, we walk you through each step in the workflow.
## Deploy 1 click
[![button](launchstack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?stackName=comprehend-active-learning&templateURL=https://aws-ml-blog.s3.amazonaws.com/artifacts/comprehend-a2i-active-learning/comprehend-active-learning-infra.yml)




## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

