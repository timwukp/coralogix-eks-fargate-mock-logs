#!/usr/bin/env python3
"""
Generate 1000 realistic Coralogix EKS Fargate log entries for troubleshooting demonstration
with Amazon Q Developer CLI.

This script creates mock logs that represent common scenarios in EKS Fargate environments:
- Application logs (nginx, user-service, payment-service)
- System logs (coredns, aws-load-balancer-controller)
- Infrastructure logs (istio-proxy, fluent-bit, prometheus)
- Database logs (postgres, redis)
- Error scenarios (connection failures, timeouts, 5xx errors)
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Base timestamp
BASE_TIME = datetime(2025, 7, 1, 7, 0, 0)

# Application configurations
APPLICATIONS = {
    "web-frontend": {
        "containers": ["nginx", "app"],
        "namespace": "web-frontend",
        "pod_prefix": "nginx-deployment-7d4c8f9b6d",
        "host_ip": "172.31.45.123"
    },
    "user-service": {
        "containers": ["app", "istio-proxy"],
        "namespace": "user-service", 
        "pod_prefix": "user-service-deployment-5f8b9c7d6e",
        "host_ip": "172.31.45.124"
    },
    "payment-service": {
        "containers": ["app", "istio-proxy"],
        "namespace": "payment-service",
        "pod_prefix": "payment-service-deployment-8e9f0a1b2c",
        "host_ip": "172.31.45.127"
    },
    "kube-system": {
        "containers": ["coredns", "aws-load-balancer-controller"],
        "namespace": "kube-system",
        "pod_prefix": "coredns-5d78c9899d",
        "host_ip": "172.31.45.125"
    },
    "monitoring": {
        "containers": ["prometheus", "grafana"],
        "namespace": "monitoring",
        "pod_prefix": "prometheus-server-7c8d9e0f1g",
        "host_ip": "172.31.45.126"
    },
    "database": {
        "containers": ["postgres", "postgres-exporter"],
        "namespace": "database",
        "pod_prefix": "postgres-primary",
        "host_ip": "172.31.45.130"
    },
    "redis": {
        "containers": ["redis", "redis-exporter"],
        "namespace": "redis",
        "pod_prefix": "redis-master",
        "host_ip": "172.31.45.131"
    },
    "logging": {
        "containers": ["fluent-bit"],
        "namespace": "logging",
        "pod_prefix": "fluent-bit-daemonset",
        "host_ip": "172.31.45.132"
    },
    "istio-system": {
        "containers": ["istio-proxy", "pilot"],
        "namespace": "istio-system",
        "pod_prefix": "istio-proxy",
        "host_ip": "172.31.45.128"
    },
    "cert-manager": {
        "containers": ["cert-manager", "webhook"],
        "namespace": "cert-manager",
        "pod_prefix": "cert-manager-5s6t7u8v9w",
        "host_ip": "172.31.45.134"
    }
}

# Log message templates
LOG_TEMPLATES = {
    "nginx": {
        "INFO": [
            '172.31.45.{ip} - - [{timestamp}] "GET /health HTTP/1.1" 200 2 "-" "kube-probe/1.28"',
            '172.31.45.{ip} - - [{timestamp}] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"',
            '172.31.45.{ip} - - [{timestamp}] "POST /api/login HTTP/1.1" 200 567 "-" "curl/7.68.0"'
        ],
        "ERROR": [
            '[error] 1#1: *{id} connect() failed (111: Connection refused) while connecting to upstream',
            '[error] 1#1: *{id} upstream timed out (110: Connection timed out) while connecting to upstream',
            '[error] 1#1: *{id} no live upstreams while connecting to upstream'
        ]
    },
    "app": {
        "INFO": [
            '{{"level":"info","msg":"Starting {service} service","version":"v{version}","port":{port}}}',
            '{{"level":"info","msg":"Processing request","request_id":"req-{id}","user_id":"user-{user_id}"}}',
            '{{"level":"info","msg":"Request completed","request_id":"req-{id}","duration_ms":{duration}}}'
        ],
        "ERROR": [
            '{{"level":"error","msg":"Database connection failed","error":"dial tcp 172.31.45.200:5432: connect: connection refused","retry_count":{retry}}}',
            '{{"level":"error","msg":"Request failed","request_id":"req-{id}","error":"{error}","status_code":{status}}}',
            '{{"level":"error","msg":"Timeout occurred","request_id":"req-{id}","timeout_ms":{timeout}}}'
        ]
    },
    "coredns": {
        "INFO": [
            '[INFO] 172.31.45.{ip}:53 - {id} "A IN {domain}. udp 32 false 512" NOERROR qr,rd,ra 76 0.{duration}s',
            '[INFO] 172.31.45.{ip}:53 - {id} "AAAA IN {domain}. udp 32 false 512" NOERROR qr,rd,ra 76 0.{duration}s'
        ],
        "ERROR": [
            '[ERROR] plugin/errors: 2 {domain}. A: read udp 172.31.45.{ip}:53->8.8.8.8:53: i/o timeout',
            '[ERROR] plugin/errors: 2 {domain}. A: no such host'
        ]
    },
    "postgres": {
        "INFO": [
            'LOG:  connection received: host=172.31.45.{ip} port={port}',
            'LOG:  connection authorized: user={user} database={db}',
            'LOG:  statement: SELECT * FROM {table} WHERE id = {id}'
        ],
        "ERROR": [
            'ERROR:  relation "{table}" does not exist at character {pos}',
            'ERROR:  duplicate key value violates unique constraint "{constraint}"',
            'FATAL:  password authentication failed for user "{user}"'
        ]
    },
    "redis": {
        "INFO": [
            '* Ready to accept connections',
            '* DB loaded from disk: {time} seconds',
            '* Background saving started by pid {pid}'
        ],
        "WARN": [
            '# WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.',
            '# WARNING: overcommit_memory is set to 0! Background save may fail under low memory condition.'
        ]
    },
    "fluent-bit": {
        "INFO": [
            '[engine] started (pid=1)',
            '[input:tail:tail.0] inotify_fs_add(): inode={inode} watch_fd={fd} name=/var/log/containers/{container}.log',
            '[output:http:http.0] coralogix.com:443, HTTP status=200 OK'
        ],
        "ERROR": [
            '[output:http:http.0] coralogix.com:443, HTTP status=429 Too Many Requests',
            '[output:http:http.0] coralogix.com:443, HTTP status=500 Internal Server Error',
            '[input:tail:tail.0] error scanning path /var/log/containers/*.log'
        ]
    },
    "istio-proxy": {
        "INFO": [
            '"GET /api/users HTTP/1.1" 200 - 0 {size} {duration} - "172.31.45.{ip}" "Mozilla/5.0" "{trace_id}" "{service}.{namespace}.svc.cluster.local:{port}" "172.31.45.{target_ip}:{port}"'
        ],
        "ERROR": [
            '"GET /api/users HTTP/1.1" 503 UF,URX upstream_reset_before_response_started{{connection_failure}} - "-" 0 95 {duration} - "172.31.45.{ip}" "Mozilla/5.0" "{trace_id}" "{service}.{namespace}.svc.cluster.local:{port}" "172.31.45.{target_ip}:{port}"'
        ]
    }
}

def generate_random_id(length: int = 8) -> str:
    """Generate random alphanumeric ID"""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_container_id() -> str:
    """Generate realistic container ID"""
    return f"containerd://{generate_random_id(64)}"

def generate_log_entry(index: int) -> Dict[str, Any]:
    """Generate a single log entry"""
    # Calculate timestamp
    timestamp = BASE_TIME + timedelta(seconds=index)
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    
    # Select random application and container
    app_name = random.choice(list(APPLICATIONS.keys()))
    app_config = APPLICATIONS[app_name]
    container_name = random.choice(app_config["containers"])
    
    # Generate pod name
    pod_suffix = generate_random_id(5)
    pod_name = f"{app_config['pod_prefix']}-{pod_suffix}"
    
    # Select severity (weighted towards INFO)
    severity = random.choices(["INFO", "WARN", "ERROR"], weights=[70, 20, 10])[0]
    
    # Generate log message based on container type
    if container_name in LOG_TEMPLATES:
        templates = LOG_TEMPLATES[container_name].get(severity, LOG_TEMPLATES[container_name]["INFO"])
        template = random.choice(templates)
        
        # Fill template variables
        log_text = template.format(
            ip=random.randint(100, 200),
            timestamp=timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000"),
            id=random.randint(1000, 9999),
            service=app_name.split('-')[0],
            version=f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
            port=random.choice([8080, 3000, 5432, 6379, 9090]),
            user_id=random.randint(10000, 99999),
            duration=random.randint(10, 5000),
            retry=random.randint(1, 5),
            error=random.choice(["timeout", "connection refused", "invalid request", "unauthorized"]),
            status=random.choice([400, 401, 403, 404, 500, 502, 503, 504]),
            timeout=random.randint(1000, 30000),
            domain=random.choice(["example.com", "api.example.com", "db.example.com"]),
            user=random.choice(["postgres", "app_user", "readonly"]),
            db=random.choice(["users", "products", "orders"]),
            table=random.choice(["users", "products", "orders", "sessions"]),
            pos=random.randint(10, 100),
            constraint=f"pk_{random.choice(['users', 'products', 'orders'])}",
            time=round(random.uniform(0.1, 5.0), 3),
            pid=random.randint(1000, 9999),
            inode=random.randint(100000, 999999),
            fd=random.randint(10, 99),
            container=f"{app_name}-{generate_random_id(8)}",
            size=random.randint(100, 10000),
            trace_id=f"{generate_random_id(8)}-{generate_random_id(4)}-{generate_random_id(4)}",
            namespace=app_config["namespace"],
            target_ip=random.randint(100, 200)
        )
    else:
        # Generic log message
        log_text = f"Generic log message for {container_name} at {timestamp_str}"
    
    # Create log entry
    log_entry = {
        "timestamp": timestamp_str,
        "applicationName": app_config["namespace"],
        "subsystemName": container_name,
        "severity": severity,
        "text": log_text,
        "json": {
            "kubernetes": {
                "namespace_name": app_config["namespace"],
                "pod_name": pod_name,
                "container_name": container_name,
                "container_id": generate_container_id(),
                "host": f"fargate-ip-{app_config['host_ip'].replace('.', '-')}.us-west-2.compute.internal",
                "labels": {
                    "app": app_name,
                    "version": f"v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
                    "environment": random.choice(["production", "staging", "development"])
                }
            },
            "log": log_text,
            "stream": "stdout" if severity == "INFO" else "stderr",
            "time": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
        }
    }
    
    return log_entry

def main():
    """Generate 1000 log entries and save to file"""
    print("Generating 1000 Coralogix EKS Fargate mock log entries...")
    
    logs = []
    for i in range(1000):
        if i % 100 == 0:
            print(f"Generated {i} logs...")
        logs.append(generate_log_entry(i))
    
    # Save to file
    output_file = "coralogix_eks_fargate_logs_1000.json"
    with open(output_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"Successfully generated 1000 log entries and saved to {output_file}")
    print(f"File size: {len(json.dumps(logs, indent=2))} bytes")
    
    # Print sample entries
    print("\nSample log entries:")
    for i in [0, 250, 500, 750, 999]:
        print(f"\nEntry {i+1}:")
        print(f"  Timestamp: {logs[i]['timestamp']}")
        print(f"  Application: {logs[i]['applicationName']}")
        print(f"  Container: {logs[i]['subsystemName']}")
        print(f"  Severity: {logs[i]['severity']}")
        print(f"  Text: {logs[i]['text'][:100]}...")

if __name__ == "__main__":
    main()