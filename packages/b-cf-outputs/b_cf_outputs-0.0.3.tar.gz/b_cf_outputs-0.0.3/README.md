# B.CfOutputs

A python based library to list AWS Cloud Formation stack outputs.

#### Description

Sometimes it is very convenient to list all outputs of all stacks
(especially programmatically). There is no API or SDK command to 
conveniently do this. Therefore, we have created this library to
easily get all of the outputs of stacks.

#### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

#### Related technology

- Python 3
- AWS CDK
- AWS CloudFormation

#### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS and CloudFormation.

#### Useful sources

- Read more about Cloud Formation:<br>
https://docs.aws.amazon.com/cloudformation/index.html

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b-cf-outputs
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

Create a boto3 session:
```python
import boto3
session = boto3.session.Session('key', 'secret')
```

List available Cloud Formation stacks:
```python
from b_cf_outputs.cf_stacks import CfStacks
stacks = CfStacks(session).get_stacks()
```

List outputs from stacks:
```python
from b_cf_outputs.cf_outputs import CfOutputs
CfOutputs(session).get_outputs()
```

#### Testing

The project has tests that can be run. Simply run:

```
pytest
```

#### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
