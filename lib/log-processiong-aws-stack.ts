import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as firehose from 'aws-cdk-lib/aws-kinesisfirehose';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class LogProcessiongAwsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 bucket
    const logBucket = new s3.Bucket(this, 'LogBucket', {
      bucketName: 'my-log-bucket-' + this.account,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // Create Lambda function for data transformation
    const processingFunction = new lambda.Function(this, 'ProcessingFunction', {
      runtime: lambda.Runtime.PYTHON_3_8,
      handler: 'index.lambda_handler',
      code: lambda.Code.fromAsset('lambda'),
    });

    // Create IAM role for Firehose
    const firehoseRole = new iam.Role(this, 'FirehoseRole', {
      assumedBy: new iam.ServicePrincipal('firehose.amazonaws.com'),
    });

    // Grant Firehose permissions to invoke Lambda and write to S3
    processingFunction.grantInvoke(firehoseRole);
    logBucket.grantWrite(firehoseRole);

    // Create Firehose delivery stream
    const deliveryStream = new firehose.CfnDeliveryStream(this, 'LogDeliveryStream', {
      deliveryStreamName: 'log-delivery-stream',
      deliveryStreamType: 'DirectPut',
      extendedS3DestinationConfiguration: {
        bucketArn: logBucket.bucketArn,
        roleArn: firehoseRole.roleArn,
        bufferingHints: {
          intervalInSeconds: 60,
          sizeInMBs: 1
        },
        processingConfiguration: {
          enabled: true,
          processors: [{
            type: 'Lambda',
            parameters: [{
              parameterName: 'LambdaArn',
              parameterValue: processingFunction.functionArn,
            }],
          }],
        },
      },
    });
  }
}