# Kinesis Logger Stream Handler

This package contains 

AwsSessionManagement - handles AWS Session with AWS Temp credentials by Assuming a given Role
                       it renews the temp credentials when needed

AWS Kinesis Logger StreamHandler - a logging streamhandler which can send logs to AWS Kinesis


Usage:

```
def get_kinesis_client(aws_access_key_id, aws_secret_access_key, aws_session_token):
    logger.info("creating/updating kinesis client ...")
    kinesis = boto3.client('kinesis', region_name=get_region(),
                           aws_access_key_id = aws_access_key_id,
                           aws_secret_access_key = aws_secret_access_key,
                           aws_session_token = aws_session_token)
    logger.info("returning new kinesis client")
    return kinesis


logger = logging.getLogger("my-package")
logger.setLevel(logging.INFO)

kinesisAwsSessionManagement = AwsSessionManagement(role_arn='roleArnValue',
                                                   external_id='externalIdValue',
                                                    func=get_kinesis_client,
                                                    role_session_name="KinesisSession")

kinesis_stream_handler = KinesisDataStreamHandler(kinesis_stream_name, 'subsystem_value', 'component_value', 'action_value', 'project_name', 'env', 'version', kinesisAwsSessionManagement)

kinesis_stream_handler.setLevel(logLevel)
logger.addHandler(kinesis_stream_handler)

```

Now, every logging call will send the logs both to console and kinesis data stream with a given 'kinesis_stream_name' 