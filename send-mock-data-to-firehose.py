import boto3
import json
import time
from  mock_container_logs import generate_mock_logs
# Create a Kinesis Firehose client
firehose = boto3.client('firehose', region_name='us-east-1')

def send_to_firehose(data, stream_name):
    response = firehose.put_record(
        DeliveryStreamName=stream_name,
        Record={'Data': json.dumps(data)}
    )
    return response

# Main execution
if __name__ == "__main__":
    stream_name = "log-delivery-stream"
    
    while True:
        # Generate a single log entry
        log_entry = generate_mock_logs(1)[0]
        
        # Send the log entry to Firehose
        response = send_to_firehose(log_entry, stream_name)
        
        print(f"Sent log entry to Firehose. Response: {response}")
        
        # Wait for a short time before sending the next log
        time.sleep(1)
