import json
import random
import datetime
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_log_entry():
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    containers = ["web-app", "database", "cache", "auth-service"]
    actions = ["Started", "Stopped", "Restarted", "Scaled", "Updated"]
    
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "level": random.choice(log_levels),
        "container": random.choice(containers),
        "message": f"{random.choice(actions)} container",
        "details": {
            "ip": f"192.168.1.{random.randint(1, 255)}",
            "port": random.randint(1000, 9999),
            "password": generate_random_string(16),  # Generate a random 16-character password
            "api_key": generate_random_string(32)    # Generate a random 32-character API key
        }
    }

def generate_mock_logs(num_entries):
    return [generate_log_entry() for _ in range(num_entries)]

# Generate 10 mock log entries
mock_logs = generate_mock_logs(10)

# Print the mock logs
print(json.dumps(mock_logs, indent=2))
