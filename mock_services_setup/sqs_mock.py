from contextlib import contextmanager

# Use a context manager to help handle setup/teardown automatically before/after tests are run
@contextmanager
def sqs_setup(sqs_resource, queue_name):
    sqs_resource.create_queue(QueueName=queue_name)
    yield

def SQS_Queue_Mock(sqs_resource, queueName):
    with sqs_setup(sqs_resource, queueName):
        return sqs_resource.get_queue_by_name(QueueName=queueName)