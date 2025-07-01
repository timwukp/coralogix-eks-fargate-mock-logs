# Coralogix EKS Fargate Mock Logs - Troubleshooting Guide

## Overview

This repository contains 1000 realistic mock log entries from a Coralogix-monitored Amazon EKS Fargate environment. These logs are designed to demonstrate how Amazon Q Developer CLI can help with troubleshooting common issues in containerized applications.

## Generated Files

1. **`coralogix_eks_fargate_logs_1000.json`** - 1000 mock log entries (~917KB)
2. **`generate_coralogix_logs.py`** - Python script used to generate the logs
3. **`analyze_logs.py`** - Analysis script to show log statistics and patterns
4. **`README.md`** - This documentation

## Log Structure

Each log entry follows the Coralogix format with EKS Fargate metadata:

```json
{
  "timestamp": "2025-07-01T07:00:00.000Z",
  "applicationName": "web-frontend",
  "subsystemName": "nginx",
  "severity": "INFO|WARN|ERROR",
  "text": "Actual log message content",
  "json": {
    "kubernetes": {
      "namespace_name": "web-frontend",
      "pod_name": "nginx-deployment-7d4c8f9b6d-x7k2m",
      "container_name": "nginx",
      "container_id": "containerd://...",
      "host": "fargate-ip-172-31-45-123.us-west-2.compute.internal",
      "labels": {
        "app": "nginx",
        "version": "v1.21.0",
        "environment": "production"
      }
    },
    "log": "Raw log message",
    "stream": "stdout|stderr",
    "time": "2025-07-01T07:00:00.000000Z"
  }
}
```

## Applications and Services Included

The mock logs represent a realistic microservices architecture:

### Frontend Services
- **web-frontend**: Nginx reverse proxy with health checks and upstream connection issues
- **api-gateway**: Envoy proxy with configuration and routing problems

### Backend Services  
- **user-service**: Go/Node.js application with database connectivity issues
- **payment-service**: Payment processing service with business logic errors

### Infrastructure Services
- **kube-system**: CoreDNS, AWS Load Balancer Controller
- **istio-system**: Service mesh proxy logs with traffic routing issues
- **monitoring**: Prometheus scraping failures and alerts
- **logging**: Fluent Bit with Coralogix integration issues
- **cert-manager**: TLS certificate management problems

### Data Services
- **database**: PostgreSQL with connection and query errors
- **redis**: Redis cache with memory and connection warnings

## Quick Start

### Generate New Logs
```bash
python3 generate_coralogix_logs.py
```

### Analyze Existing Logs
```bash
python3 analyze_logs.py
```

## Common Issues Represented

### 1. Connection Failures
```bash
# Find connection refused errors
q chat "Show me all connection refused errors from the logs"
```

### 2. Database Issues
```bash
# Analyze database connectivity problems
q chat "What database errors are occurring and what might be causing them?"
```

### 3. Service Mesh Problems
```bash
# Investigate Istio proxy errors
q chat "Analyze the istio-proxy logs for service communication issues"
```

### 4. Load Balancer Issues
```bash
# Check AWS Load Balancer Controller problems
q chat "What load balancer issues are present in the logs?"
```

### 5. DNS Resolution Problems
```bash
# Examine CoreDNS logs
q chat "Are there any DNS resolution failures in the logs?"
```

## Troubleshooting Scenarios with Amazon Q Developer CLI

### Scenario 1: Application Performance Issues

```bash
# Load the logs and ask Q to analyze performance
q chat "I'm seeing slow response times. Can you analyze these Coralogix logs and identify performance bottlenecks?"

# Follow up with specific questions
q chat "What are the most common timeout errors and which services are affected?"
```

### Scenario 2: Service Discovery Problems

```bash
# Investigate service connectivity
q chat "Users are reporting that the application is down. Can you help me trace the issue through these logs?"

# Focus on specific services
q chat "Check if the user-service can connect to the database based on these logs"
```

### Scenario 3: Infrastructure Issues

```bash
# Analyze infrastructure components
q chat "Are there any Kubernetes infrastructure issues visible in these logs?"

# Check specific components
q chat "What issues are present with the AWS Load Balancer Controller?"
```

### Scenario 4: Security and Certificate Issues

```bash
# Investigate TLS/certificate problems
q chat "Are there any certificate or TLS-related errors in the logs?"

# Check cert-manager specifically
q chat "What certificate management issues are occurring?"
```

### Scenario 5: Resource and Scaling Issues

```bash
# Look for resource constraints
q chat "Are there any signs of resource exhaustion or scaling issues in these logs?"

# Check for rate limiting
q chat "Are we hitting any rate limits with external services like Coralogix?"
```

## Advanced Analysis Examples

### Error Pattern Analysis
```bash
q chat "Group the errors by type and frequency. What are the top 5 most common issues?"
```

### Timeline Analysis
```bash
q chat "Create a timeline of critical errors. Are there any patterns or cascading failures?"
```

### Service Dependency Mapping
```bash
q chat "Based on these logs, can you map out the service dependencies and identify single points of failure?"
```

### Root Cause Analysis
```bash
q chat "I see multiple services failing around 07:00:02. Can you help me trace the root cause?"
```

## Log Statistics

- **Total entries**: 1000 logs
- **Time span**: ~17 minutes (2025-07-01 07:00:00 to 07:16:39)
- **File size**: ~917KB
- **Applications**: 10 different services
- **Container types**: 15+ different containers
- **Severity distribution**: 70% INFO, 20% WARN, 10% ERROR

## Realistic Error Scenarios

### Network Issues
- Connection refused errors
- Upstream timeouts
- DNS resolution failures
- Load balancer target group issues

### Application Errors
- Database connection failures
- Authentication/authorization errors
- Business logic failures (insufficient funds, etc.)
- Configuration errors

### Infrastructure Problems
- Certificate expiration/validation issues
- Resource exhaustion
- Rate limiting
- Service mesh configuration problems

## Using with Amazon Q Developer CLI

1. **Load the logs**: Download the JSON file to your working directory
2. **Start analysis**: Use `q chat` with natural language queries
3. **Iterate**: Ask follow-up questions based on initial findings
4. **Cross-reference**: Compare findings across different services and timeframes

## Example Q Chat Session

```bash
# Initial analysis
q chat "I have Coralogix logs from an EKS Fargate cluster. Can you help me identify the most critical issues?"

# Follow-up based on response
q chat "The user-service seems to be having database connection issues. Can you show me all related errors and suggest troubleshooting steps?"

# Deeper investigation
q chat "What AWS-specific issues are present? Focus on load balancer and Fargate-related problems."

# Solution-oriented questions
q chat "Based on these error patterns, what would be your recommended action plan to resolve these issues?"
```

## Best Practices for Log Analysis

1. **Start broad, then narrow**: Begin with general queries, then focus on specific services or error types
2. **Look for patterns**: Ask Q to identify recurring issues or time-based patterns
3. **Consider dependencies**: Understand how service failures cascade through the system
4. **Prioritize by impact**: Focus on errors affecting user-facing services first
5. **Validate hypotheses**: Use Q to test your theories about root causes

## Contributing

Feel free to extend the log generator script to add new services, error patterns, or scenarios that would be useful for demonstrating Amazon Q Developer CLI capabilities.

## License

This project is provided as-is for demonstration purposes. The generated logs are synthetic and do not contain any real customer data.

---

This mock dataset provides a comprehensive foundation for demonstrating Amazon Q Developer CLI's capabilities in log analysis and troubleshooting containerized applications in AWS environments.