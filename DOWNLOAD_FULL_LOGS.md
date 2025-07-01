# Download Full Log File

## Full Dataset Available

The complete dataset with **1000 log entries** (~917KB) is available for download. Due to GitHub's file size limitations, the full file is not included in this repository.

## How to Generate the Full Dataset

You can generate the complete 1000-entry log file using the provided Python script:

```bash
# Clone this repository
git clone https://github.com/timwukp/coralogix-eks-fargate-mock-logs.git
cd coralogix-eks-fargate-mock-logs

# Run the generator script
python3 generate_coralogix_logs.py

# This will create: coralogix_eks_fargate_logs_1000.json
```

## What You Get

- **1000 realistic log entries** spanning ~17 minutes
- **10 different applications** (web-frontend, user-service, payment-service, etc.)
- **15+ container types** (nginx, app, istio-proxy, fluent-bit, etc.)
- **Realistic error scenarios** including:
  - Connection failures
  - Database connectivity issues
  - Service mesh problems
  - DNS resolution failures
  - Certificate/TLS issues
  - Rate limiting
  - Resource constraints

## File Statistics

- **Total entries**: 1000 logs
- **Time span**: 2025-07-01 07:00:00 to 07:16:39 UTC
- **File size**: ~917KB
- **Format**: JSON array with Coralogix-compatible structure
- **Severity distribution**: 70% INFO, 20% WARN, 10% ERROR

## Sample Data

The repository includes `coralogix_eks_fargate_logs_sample.json` with a smaller sample of key error scenarios for quick testing.

## Analysis

After generating the full file, you can analyze it using:

```bash
python3 analyze_logs.py
```

This will show statistics about applications, containers, error patterns, and provide examples for troubleshooting with Amazon Q Developer CLI.

## Using with Amazon Q Developer CLI

Once you have the full log file, you can use it for troubleshooting demonstrations:

```bash
q chat "I have Coralogix logs from an EKS Fargate cluster. Can you help me identify the most critical issues?"
q chat "What database connectivity problems do you see in these logs?"
q chat "Help me troubleshoot the service mesh issues"
q chat "Are there any patterns in the error logs that suggest cascading failures?"
```

The logs are structured to provide realistic scenarios for demonstrating Amazon Q Developer CLI's troubleshooting capabilities in containerized AWS environments.