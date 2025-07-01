# Coralogix EKS Fargate Mock Logs Demo

This repository contains a comprehensive demonstration of Amazon Q Developer CLI troubleshooting capabilities using realistic mock Coralogix logs from an EKS Fargate cluster.

## 📁 Repository Contents

```
coralogix-eks-fargate-mock-logs/
├── README.md                                    # This documentation
├── generate_coralogix_logs.py                  # Log generator script
├── analyze_logs.py                             # Log analysis tool
├── troubleshooting_guide.md                    # Detailed troubleshooting examples
├── coralogix_eks_fargate_logs_sample.json      # Sample logs (100 entries)
├── coralogix_eks_fargate_logs_1000.json        # Full dataset (1000 entries)
└── DOWNLOAD_FULL_LOGS.md                       # Download instructions
```

## 🚀 Quick Start

### 1. Generate Mock Logs
```bash
python3 generate_coralogix_logs.py
```

This creates `coralogix_eks_fargate_logs_1000.json` with 1000 realistic log entries.

### 2. Analyze the Logs
```bash
python3 analyze_logs.py
```

This provides detailed statistics and patterns in the generated logs.

### 3. Use with Amazon Q Developer CLI
```bash
q chat "I have Coralogix logs from an EKS Fargate cluster. Can you help me identify the most critical issues?"
```

## 📊 What's Included

### Applications & Services
- **web-frontend**: Nginx + application containers
- **user-service**: Microservice with Istio sidecar
- **payment-service**: Payment processing service
- **database**: PostgreSQL database
- **redis**: Redis cache
- **monitoring**: Prometheus + Grafana
- **kube-system**: Core Kubernetes services
- **istio-system**: Service mesh components
- **cert-manager**: Certificate management
- **logging**: Fluent-bit log collection

### Error Scenarios
- Database connection failures
- Service mesh configuration issues
- DNS resolution problems
- Certificate/TLS errors
- Rate limiting
- Resource constraints
- Network timeouts
- Load balancer issues

### Log Structure
Each log entry follows Coralogix format with:
- Timestamp
- Application name
- Subsystem (container)
- Severity (INFO/WARN/ERROR)
- Message text
- Kubernetes metadata (pod, namespace, labels)
- AWS Fargate metadata

## 🔍 Troubleshooting Examples

### Database Issues
```bash
q chat "What database connectivity problems do you see in these logs?"
q chat "Help me troubleshoot the PostgreSQL connection failures"
```

### Service Mesh Problems
```bash
q chat "Analyze the Istio service mesh errors in these logs"
q chat "What service-to-service communication issues are present?"
```

### Infrastructure Issues
```bash
q chat "What Kubernetes infrastructure problems do you see?"
q chat "Help me understand the EKS Fargate pod failures"
```

### Performance Analysis
```bash
q chat "What performance bottlenecks are indicated in these logs?"
q chat "Are there any resource constraint issues?"
```

## 📈 Log Statistics

The generated logs include:
- **1000 total entries** spanning ~17 minutes
- **70% INFO, 20% WARN, 10% ERROR** severity distribution
- **10 different applications** with realistic error rates
- **15+ container types** representing a full microservices stack
- **Multiple namespaces** (default, backend, kube-system, etc.)
- **Realistic timestamps** with natural distribution

## 🛠️ Technical Details

### Log Format
```json
{
  "timestamp": "2025-07-01T07:00:15.123456Z",
  "applicationName": "user-service",
  "subsystemName": "app",
  "severity": "ERROR",
  "text": "Database connection failed (connection_pool_size: 25)",
  "json": {
    "kubernetes": {
      "namespace_name": "backend",
      "pod_name": "user-service-app-a1b2c3d4e5",
      "container_name": "app",
      "container_id": "1234567890abcdef...",
      "host": "10.0.1.123",
      "labels": {
        "app": "user-service",
        "version": "v2.1.3",
        "environment": "production",
        "tier": "backend"
      }
    },
    "aws": {
      "region": "us-west-2",
      "cluster_name": "production-eks-cluster",
      "fargate_profile": "default-profile"
    },
    "error_details": {
      "error_code": "CONNECTION_REFUSED",
      "retry_count": 3,
      "last_successful_connection": "2025-07-01T06:45:22.456789Z"
    }
  }
}
```

### Error Patterns
The logs simulate realistic production issues:
- **Connection failures**: Database, Redis, service-to-service
- **Timeouts**: Database queries, HTTP requests, DNS lookups
- **Resource issues**: Memory pressure, disk space, connection pools
- **Security**: Certificate expiration, TLS handshake failures
- **Service mesh**: Istio proxy errors, configuration issues
- **Infrastructure**: Pod startup failures, load balancer issues

## 🎯 Use Cases

### 1. Amazon Q Developer CLI Demonstrations
Show how natural language queries can identify and troubleshoot complex issues in containerized applications.

### 2. Log Analysis Training
Practice identifying patterns and root causes in realistic microservices logs.

### 3. Troubleshooting Workflows
Demonstrate systematic approaches to diagnosing production issues.

### 4. Tool Integration
Show how Amazon Q can work with existing log analysis workflows.

## 📝 Sample Queries for Amazon Q

### Root Cause Analysis
- "What's causing the most errors in this EKS cluster?"
- "Are there any cascading failures indicated in these logs?"
- "Help me identify the root cause of the service outages"

### Specific Service Issues
- "What's wrong with the payment-service?"
- "Why is the user-service having database issues?"
- "What Istio configuration problems do you see?"

### Infrastructure Problems
- "Are there any Kubernetes resource issues?"
- "What DNS or networking problems are present?"
- "Help me understand the load balancer failures"

### Performance Analysis
- "What services are experiencing high latency?"
- "Are there any resource bottlenecks?"
- "What's causing the slow database queries?"

## 🔧 Customization

### Modify Log Generation
Edit `generate_coralogix_logs.py` to:
- Change the number of logs generated
- Adjust error rates for different services
- Add new applications or containers
- Modify time ranges or patterns

### Add New Error Scenarios
Extend the `LOG_MESSAGES` dictionary with:
- New error types
- Service-specific messages
- Custom error details

### Adjust Analysis
Modify `analyze_logs.py` to:
- Add new analysis patterns
- Change reporting formats
- Include additional metrics

## 🤝 Contributing

This demo is designed to showcase Amazon Q Developer CLI capabilities. Feel free to:
- Add new error scenarios
- Improve log realism
- Enhance analysis capabilities
- Create additional troubleshooting examples

## 📚 Related Resources

- [Amazon Q Developer CLI Documentation](https://docs.aws.amazon.com/amazonq/)
- [EKS Fargate Logging Best Practices](https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html)
- [Coralogix Documentation](https://coralogix.com/docs/)
- [Kubernetes Troubleshooting Guide](https://kubernetes.io/docs/tasks/debug-application-cluster/)

---

**Note**: These are mock logs created for demonstration purposes. They simulate realistic scenarios but are not from actual production systems.