
# AWS Lambda - Python Unit Test

## Problem Statement
1. `AWS Lambda` is commonly being used together with other AWS Services such as `DynamoDB`, `S3` and `SQS`. 
2. Conventional `Python` Unit Testing is not sufficient to perform unit test on `AWS Lambda Python` as it requires integration with AWS Services.

---
## This Repository
1. Provides an example how AWS Services (e.g. *DynamoDB*) can be mocked to allow Unit Testing on `AWS Lambda Python`. 
2. Provides an example how `AWS CDK` is used together in this project as demostration of `IAC` together with `AWS Lambda Python` Source Code.

---
## Dependencies Required
requirements-test.txt
```
pytest==6.2.5
pytest-cov==3.0.0
pytest-mock==3.8.2
requests-mock==1.10.0
moto[all]==4.0.1
```

---
## Pytest Command
```
python3 -m pytest lambda/functions_tests/*/test_*.py --capture=sys --cov=lambda/functions --cov-fail-under=95 --cov-report=term-missing
```

---

# CDK Python Project Setup

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
