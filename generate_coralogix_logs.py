#!/usr/bin/env python3
"""
Coralogix EKS Fargate Mock Log Generator

This script generates realistic mock logs that simulate Coralogix logs from an EKS Fargate cluster.
The logs include various microservices, error scenarios, and Kubernetes metadata.

Usage:
    python3 generate_coralogix_logs.py

Output:
    coralogix_eks_fargate_logs_1000.json - 1000 realistic log entries
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configuration
NUM_LOGS = 1000
START_TIME = datetime(2025, 7, 1, 7, 0, 0)  # UTC
TIME_SPAN_MINUTES = 17

# Application and service definitions
APPLICATIONS = {
    "web-frontend": {
        "containers": ["nginx", "app"],
        "namespaces": ["default", "frontend"],
        "error_rate": 0.15
    },
    "user-service": {
        "containers": ["app", "istio-proxy"],
        "namespaces": ["default", "backend"],
        "error_rate": 0.12
    },
    "payment-service": {
        "containers": ["app", "istio-proxy"],
        "namespaces": ["default", "backend"],
        "error_rate": 0.18
    },
    "kube-system": {
        "containers": ["coredns", "aws-load-balancer-controller"],
        "namespaces": ["kube-system"],
        "error_rate": 0.08
    },
    "monitoring": {
        "containers": ["prometheus", "grafana"],
        "namespaces": ["monitoring"],
        "error_rate": 0.05
    },
    "database": {
        "containers": ["postgres"],
        "namespaces": ["database"],
        "error_rate": 0.20
    },
    "redis": {
        "containers": ["redis"],
        "namespaces": ["cache"],
        "error_rate": 0.10
    },
    "logging": {
        "containers": ["fluent-bit"],
        "namespaces": ["kube-system", "logging"],
        "error_rate": 0.07
    },
    "istio-system": {
        "containers": ["istio-proxy", "pilot"],
        "namespaces": ["istio-system"],
        "error_rate": 0.09
    },
    "cert-manager": {
        "containers": ["cert-manager", "webhook"],
        "namespaces": ["cert-manager"],
        "error_rate": 0.06
    }
}

# Log message templates
LOG_MESSAGES = {
    "INFO": [
        "Request processed successfully",
        "Health check passed",
        "Service started successfully",
        "Configuration loaded",
        "Database connection established",
        "Cache hit for key",
        "User authenticated successfully",
        "Payment processed",
        "Order created",
        "Metrics collected",
        "Certificate renewed",
        "Pod started successfully",
        "Service mesh configuration applied",
        "Load balancer health check passed"
    ],
    "WARN": [
        "High memory usage detected",
        "Slow database query detected",
        "Rate limit approaching",
        "Certificate expires soon",
        "Disk space running low",
        "Connection pool nearly exhausted",
        "Cache miss rate high",
        "Service response time elevated",
        "Retry attempt failed",
        "Configuration drift detected",
        "Pod restart detected",
        "Network latency increased"
    ],
    "ERROR": [
        "Database connection failed",
        "Service unavailable",
        "Authentication failed",
        "Payment processing failed",
        "Internal server error",
        "Connection timeout",
        "Certificate validation failed",
        "DNS resolution failed",
        "Service mesh configuration error",
        "Load balancer health check failed",
        "Pod failed to start",
        "Resource quota exceeded",
        "Network policy violation",
        "TLS handshake failed",
        "Upstream service unreachable",
        "Database query timeout",
        "Cache connection lost",
        "Service discovery failed"
    ]
}

def generate_fargate_ip():
    """Generate a realistic Fargate IP address"""
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_container_id():
    """Generate a realistic container ID"""
    return ''.join(random.choices('0123456789abcdef', k=64))

def generate_pod_name(app_name: str, container: str):
    """Generate a realistic Kubernetes pod name"""
    suffix = ''.join(random.choices('0123456789abcdef', k=10))
    return f"{app_name}-{container}-{suffix}"

def generate_log_entry(timestamp: datetime) -> Dict[str, Any]:
    """Generate a single log entry"""
    
    # Select application and container
    app_name = random.choice(list(APPLICATIONS.keys()))
    app_config = APPLICATIONS[app_name]
    container = random.choice(app_config["containers"])
    namespace = random.choice(app_config["namespaces"])
    
    # Determine severity based on error rate
    if random.random() < app_config["error_rate"]:
        if random.random() < 0.5:  # 50% ERROR, 50% WARN for problematic logs
            severity = "ERROR"
        else:
            severity = "WARN"
    else:
        severity = "INFO"
    
    # Select appropriate message
    message = random.choice(LOG_MESSAGES[severity])
    
    # Add context to some messages
    if "database" in message.lower():
        message += f" (connection_pool_size: {random.randint(5, 50)})"
    elif "timeout" in message.lower():
        message += f" (timeout: {random.randint(5, 30)}s)"
    elif "rate limit" in message.lower():
        message += f" (current: {random.randint(80, 95)}%)"
    
    # Generate pod and container metadata
    pod_name = generate_pod_name(app_name, container)
    container_id = generate_container_id()
    host_ip = generate_fargate_ip()
    
    # Create the log entry
    log_entry = {
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "applicationName": app_name,
        "subsystemName": container,
        "severity": severity,
        "text": message,
        "json": {
            "kubernetes": {
                "namespace_name": namespace,
                "pod_name": pod_name,
                "container_name": container,
                "container_id": container_id,
                "host": host_ip,
                "labels": {
                    "app": app_name,
                    "version": f"v{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                    "environment": random.choice(["production", "staging"]),
                    "tier": random.choice(["frontend", "backend", "database", "cache", "system"])
                }
            },
            "aws": {
                "region": "us-west-2",
                "cluster_name": "production-eks-cluster",
                "fargate_profile": "default-profile"
            }
        }
    }
    
    # Add additional context for specific error types
    if severity == "ERROR":
        if "database" in message.lower():
            log_entry["json"]["error_details"] = {
                "error_code": random.choice(["CONNECTION_REFUSED", "TIMEOUT", "AUTH_FAILED"]),
                "retry_count": random.randint(1, 5),
                "last_successful_connection": (timestamp - timedelta(minutes=random.randint(1, 30))).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        elif "service" in message.lower() and "unavailable" in message.lower():
            log_entry["json"]["error_details"] = {
                "upstream_service": random.choice(["user-service", "payment-service", "inventory-service"]),
                "status_code": random.choice([503, 502, 504]),
                "response_time_ms": random.randint(5000, 30000)
            }
    
    return log_entry

def generate_logs() -> List[Dict[str, Any]]:
    """Generate all log entries"""
    logs = []
    
    for i in range(NUM_LOGS):
        # Distribute logs across the time span
        minutes_offset = (i / NUM_LOGS) * TIME_SPAN_MINUTES
        timestamp = START_TIME + timedelta(minutes=minutes_offset)
        
        # Add some randomness to timestamps
        timestamp += timedelta(seconds=random.randint(-30, 30))
        
        log_entry = generate_log_entry(timestamp)
        logs.append(log_entry)
    
    # Sort by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    
    return logs

def main():
    """Main function to generate and save logs"""
    print("Generating Coralogix EKS Fargate mock logs...")
    print(f"Creating {NUM_LOGS} log entries spanning {TIME_SPAN_MINUTES} minutes")
    
    logs = generate_logs()
    
    # Save to file
    output_file = "coralogix_eks_fargate_logs_1000.json"
    with open(output_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"✅ Generated {len(logs)} log entries")
    print(f"📁 Saved to: {output_file}")
    
    # Show some statistics
    severity_counts = {}
    app_counts = {}
    
    for log in logs:
        severity = log["severity"]
        app = log["applicationName"]
        
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        app_counts[app] = app_counts.get(app, 0) + 1
    
    print("\n📊 Statistics:")
    print("Severity distribution:")
    for severity, count in sorted(severity_counts.items()):
        percentage = (count / len(logs)) * 100
        print(f"  {severity}: {count} ({percentage:.1f}%)")
    
    print(f"\nTime range: {logs[0]['timestamp']} to {logs[-1]['timestamp']}")
    print(f"Applications: {len(app_counts)} different applications")
    
    # Calculate file size
    import os
    file_size = os.path.getsize(output_file)
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

if __name__ == "__main__":
    main()