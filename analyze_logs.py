#!/usr/bin/env python3
"""
Analyze the generated Coralogix EKS Fargate mock logs to show statistics
and demonstrate the variety of scenarios included.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime

def analyze_logs():
    """Analyze the generated log file and show statistics"""
    
    # Load the logs
    with open('coralogix_eks_fargate_logs_1000.json', 'r') as f:
        logs = json.load(f)
    
    print("=== Coralogix EKS Fargate Mock Logs Analysis ===\n")
    print(f"Total log entries: {len(logs)}")
    
    # Analyze by application
    apps = Counter(log['applicationName'] for log in logs)
    print(f"\n📱 Applications ({len(apps)} total):")
    for app, count in apps.most_common():
        print(f"  {app}: {count} logs")
    
    # Analyze by container/subsystem
    containers = Counter(log['subsystemName'] for log in logs)
    print(f"\n🐳 Containers/Subsystems ({len(containers)} total):")
    for container, count in containers.most_common():
        print(f"  {container}: {count} logs")
    
    # Analyze by severity
    severities = Counter(log['severity'] for log in logs)
    print(f"\n⚠️  Severity Distribution:")
    for severity, count in severities.most_common():
        percentage = (count / len(logs)) * 100
        print(f"  {severity}: {count} logs ({percentage:.1f}%)")
    
    # Analyze error patterns
    error_logs = [log for log in logs if log['severity'] == 'ERROR']
    print(f"\n🚨 Error Analysis ({len(error_logs)} errors):")
    
    error_patterns = defaultdict(list)
    for log in error_logs:
        text = log['text'].lower()
        if 'connection refused' in text:
            error_patterns['Connection Refused'].append(log)
        elif 'timeout' in text:
            error_patterns['Timeout'].append(log)
        elif 'database' in text or 'db' in text:
            error_patterns['Database Issues'].append(log)
        elif 'upstream' in text:
            error_patterns['Upstream Issues'].append(log)
        elif 'certificate' in text or 'tls' in text:
            error_patterns['Certificate/TLS Issues'].append(log)
        else:
            error_patterns['Other Errors'].append(log)
    
    for pattern, pattern_logs in error_patterns.items():
        print(f"  {pattern}: {len(pattern_logs)} errors")
        if pattern_logs:
            # Show example
            example = pattern_logs[0]
            print(f"    Example: {example['text'][:80]}...")
    
    # Time analysis
    timestamps = [datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')) for log in logs]
    start_time = min(timestamps)
    end_time = max(timestamps)
    duration = end_time - start_time
    
    print(f"\n⏰ Time Range:")
    print(f"  Start: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  End: {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Duration: {duration}")
    
    # Kubernetes metadata analysis
    namespaces = Counter(log['json']['kubernetes']['namespace_name'] for log in logs)
    hosts = Counter(log['json']['kubernetes']['host'] for log in logs)
    
    print(f"\n☸️  Kubernetes Metadata:")
    print(f"  Unique namespaces: {len(namespaces)}")
    print(f"  Unique Fargate hosts: {len(hosts)}")
    
    # Show some interesting log samples
    print(f"\n📋 Sample Log Entries:")
    
    # Show one error from each major service
    services_shown = set()
    for log in logs:
        if log['severity'] == 'ERROR' and log['applicationName'] not in services_shown:
            services_shown.add(log['applicationName'])
            print(f"\n  🔴 {log['applicationName']}/{log['subsystemName']} ERROR:")
            print(f"     Time: {log['timestamp']}")
            print(f"     Text: {log['text'][:100]}...")
            if len(services_shown) >= 3:  # Show max 3 examples
                break
    
    print(f"\n✅ Analysis complete! Use these logs with Amazon Q Developer CLI:")
    print(f"   q chat \"Analyze these Coralogix logs and identify the top issues\"")
    print(f"   q chat \"What database connectivity problems do you see?\"")
    print(f"   q chat \"Help me troubleshoot the service mesh issues\"")

if __name__ == "__main__":
    analyze_logs()