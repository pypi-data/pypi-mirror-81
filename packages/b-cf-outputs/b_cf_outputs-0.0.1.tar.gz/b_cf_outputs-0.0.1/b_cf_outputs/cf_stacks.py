from typing import Iterator

import boto3


class CfStacks:
    """
    Class that is responsible for working with Cloud Formation stacks.
    """
    def __init__(self, boto_session: boto3.session.Session) -> None:
        """
        Constructor.

        :param boto_session: AWS SDK session instance.
        """
        self.boto_session = boto_session
        self.client = self.boto_session.client('cloudformation')

    def get_stacks(self) -> Iterator[str]:
        """
        Gets all available stacks.
        :return:
        """
        response = self.client.list_stacks()
        stacks = response['StackSummaries']

        for stack in stacks:
            yield stack['StackName']
