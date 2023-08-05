import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-fargate-fastautoscaler",
    "version": "0.2.30",
    "description": "A JSII construct lib to build AWS Fargate Fast Autoscaler",
    "license": "Apache-2.0",
    "url": "https://github.com/aws-samples/aws-fargate-fast-autoscaler.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws-samples/aws-fargate-fast-autoscaler.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_fargate_fastautoscaler",
        "cdk_fargate_fastautoscaler._jsii"
    ],
    "package_data": {
        "cdk_fargate_fastautoscaler._jsii": [
            "cdk-fargate-fastautoscaler@0.2.30.jsii.tgz"
        ],
        "cdk_fargate_fastautoscaler": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.62.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.62.0, <2.0.0",
        "aws-cdk.aws-elasticloadbalancingv2>=1.62.0, <2.0.0",
        "aws-cdk.aws-iam>=1.62.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.62.0, <2.0.0",
        "aws-cdk.aws-sns>=1.62.0, <2.0.0",
        "aws-cdk.aws-stepfunctions-tasks>=1.62.0, <2.0.0",
        "aws-cdk.aws-stepfunctions>=1.62.0, <2.0.0",
        "aws-cdk.core>=1.62.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.12.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
