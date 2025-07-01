#!/usr/bin/env python3
"""
Coralogix EKS Fargate Log Analyzer

This script analyzes the generated mock logs and provides statistics and insights
for demonstrating Amazon Q Developer CLI troubleshooting capabilities.

Usage:
    python3 analyze_logs.py [log_file]

Default log file: coralogix_eks_fargate_logs_1000.json
"""

import json
import sys
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any

def load_logs(filename: str) -> List[Dict[str, Any]]:
    """Load logs from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        print("💡 Run 'python3 generate_coralogix_logs.py' first to generate the logs.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{filename}': {e}")
        sys.exit(1)

def analyze_logs(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze logs and return statistics"""
    
    analysis = {
        "total_logs": len(logs),
        "severity_distribution": Counter(),
        "application_distribution": Counter(),
        "container_distribution": Counter(),
        "namespace_distribution": Counter(),
        "error_patterns": defaultdict(list),
        "time_range": {},
        "kubernetes_info": {
            "unique_pods": set(),
            "unique_hosts": set(),
            "environments": Counter(),
            "versions": Counter()
        }
    }
    
    timestamps = []
    
    for log in logs:
        # Basic counts
        analysis["severity_distribution"][log["severity"]] += 1
        analysis["application_distribution"][log["applicationName"]] += 1
        analysis["container_distribution"][log["subsystemName"]] += 1
        
        # Kubernetes metadata
        k8s_data = log.get("json", {}).get("kubernetes", {})
        if k8s_data:
            analysis["namespace_distribution"][k8s_data.get("namespace_name", "unknown")] += 1
            analysis["kubernetes_info"]["unique_pods"].add(k8s_data.get("pod_name", ""))
            analysis["kubernetes_info"]["unique_hosts"].add(k8s_data.get("host", ""))
            
            labels = k8s_data.get("labels", {})
            if "environment" in labels:
                analysis["kubernetes_info"]["environments"][labels["environment"]] += 1
            if "version" in labels:
                analysis["kubernetes_info"]["versions"][labels["version"]] += 1
        
        # Error pattern analysis
        if log["severity"] in ["ERROR", "WARN"]:
            error_key = f"{log['applicationName']}:{log['subsystemName']}"
            analysis["error_patterns"][error_key].append({
                "timestamp": log["timestamp"],
                "severity": log["severity"],
                "message": log["text"],
                "error_details": log.get("json", {}).get("error_details")
            })
        
        # Timestamp tracking
        timestamps.append(log["timestamp"])
    
    # Time range analysis
    if timestamps:
        analysis["time_range"] = {
            "start": min(timestamps),
            "end": max(timestamps),
            "duration_minutes": calculate_duration_minutes(min(timestamps), max(timestamps))
        }
    
    # Convert sets to counts for serialization
    analysis["kubernetes_info"]["unique_pods"] = len(analysis["kubernetes_info"]["unique_pods"])
    analysis["kubernetes_info"]["unique_hosts"] = len(analysis["kubernetes_info"]["unique_hosts"])
    
    return analysis

def calculate_duration_minutes(start_time: str, end_time: str) -> float:
    """Calculate duration between timestamps in minutes"""
    try:
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        return (end - start).total_seconds() / 60
    except:
        return 0

def print_analysis(analysis: Dict[str, Any]):
    """Print formatted analysis results"""
    
    print("🔍 CORALOGIX EKS FARGATE LOG ANALYSIS")
    print("=" * 50)
    
    # Basic statistics
    print(f"\n📊 BASIC STATISTICS")
    print(f"Total log entries: {analysis['total_logs']:,}")
    print(f"Time range: {analysis['time_range'].get('start', 'N/A')} to {analysis['time_range'].get('end', 'N/A')}")
    print(f"Duration: {analysis['time_range'].get('duration_minutes', 0):.1f} minutes")
    
    # Severity distribution
    print(f"\n🚨 SEVERITY DISTRIBUTION")
    total = analysis['total_logs']
    for severity, count in analysis['severity_distribution'].most_common():
        percentage = (count / total) * 100
        print(f"  {severity:5}: {count:4} ({percentage:5.1f}%)")
    
    # Application distribution
    print(f"\n🏗️  APPLICATION DISTRIBUTION")
    for app, count in analysis['application_distribution'].most_common():
        percentage = (count / total) * 100
        print(f"  {app:20}: {count:4} ({percentage:5.1f}%)")
    
    # Container distribution
    print(f"\n📦 CONTAINER DISTRIBUTION")
    for container, count in analysis['container_distribution'].most_common():
        percentage = (count / total) * 100
        print(f"  {container:20}: {count:4} ({percentage:5.1f}%)")
    
    # Namespace distribution
    print(f"\n🏷️  NAMESPACE DISTRIBUTION")
    for namespace, count in analysis['namespace_distribution'].most_common():
        percentage = (count / total) * 100
        print(f"  {namespace:20}: {count:4} ({percentage:5.1f}%)")
    
    # Kubernetes info
    k8s_info = analysis['kubernetes_info']
    print(f"\n☸️  KUBERNETES METADATA")
    print(f"  Unique pods: {k8s_info['unique_pods']}")
    print(f"  Unique hosts: {k8s_info['unique_hosts']}")
    print(f"  Environments: {dict(k8s_info['environments'])}")
    
    # Error patterns
    print(f"\n❌ ERROR PATTERNS (Top 10)")
    error_counts = {k: len(v) for k, v in analysis['error_patterns'].items()}
    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (error_key, count) in enumerate(sorted_errors[:10], 1):
        app, container = error_key.split(':', 1)
        print(f"  {i:2}. {app}/{container}: {count} errors")
    
    # Sample error messages
    print(f"\n🔍 SAMPLE ERROR MESSAGES")
    sample_count = 0
    for error_key, errors in analysis['error_patterns'].items():
        if sample_count >= 5:
            break
        
        error_errors = [e for e in errors if e['severity'] == 'ERROR']
        if error_errors:
            sample_error = error_errors[0]
            app, container = error_key.split(':', 1)
            print(f"  • {app}/{container}: {sample_error['message']}")
            if sample_error.get('error_details'):
                details = sample_error['error_details']
                if 'error_code' in details:
                    print(f"    └─ Error Code: {details['error_code']}")
                if 'status_code' in details:
                    print(f"    └─ Status Code: {details['status_code']}")
            sample_count += 1

def print_troubleshooting_examples():
    """Print example Amazon Q Developer CLI queries"""
    
    print(f"\n🤖 AMAZON Q DEVELOPER CLI EXAMPLES")
    print("=" * 50)
    print("Use these example queries with Amazon Q Developer CLI:")
    print()
    
    examples = [
        {
            "category": "🔍 General Analysis",
            "queries": [
                "Analyze these Coralogix logs and identify the most critical issues",
                "What are the main error patterns in these EKS Fargate logs?",
                "Show me a summary of all the problems in this log file"
            ]
        },
        {
            "category": "🗄️ Database Issues",
            "queries": [
                "What database connectivity problems do you see in these logs?",
                "Help me troubleshoot the database connection failures",
                "Are there any database timeout issues in these logs?"
            ]
        },
        {
            "category": "🕸️ Service Mesh",
            "queries": [
                "Help me troubleshoot the Istio service mesh issues",
                "What service-to-service communication problems are shown?",
                "Analyze the istio-proxy errors in these logs"
            ]
        },
        {
            "category": "🏗️ Infrastructure",
            "queries": [
                "What Kubernetes infrastructure issues do you see?",
                "Help me understand the EKS Fargate pod failures",
                "Are there any load balancer or DNS issues?"
            ]
        },
        {
            "category": "📈 Performance",
            "queries": [
                "What performance issues are indicated in these logs?",
                "Help me identify bottlenecks and slow services",
                "Are there any resource constraint problems?"
            ]
        }
    ]
    
    for example in examples:
        print(f"{example['category']}")
        for query in example['queries']:
            print(f"  q chat \"{query}\"")
        print()

def main():
    """Main function"""
    # Determine log file
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = "coralogix_eks_fargate_logs_1000.json"
    
    print(f"📁 Loading logs from: {log_file}")
    
    # Load and analyze logs
    logs = load_logs(log_file)
    analysis = analyze_logs(logs)
    
    # Print results
    print_analysis(analysis)
    print_troubleshooting_examples()
    
    print(f"\n✅ Analysis complete!")
    print(f"💡 Use the example queries above with Amazon Q Developer CLI to explore these logs.")

if __name__ == "__main__":
    main()