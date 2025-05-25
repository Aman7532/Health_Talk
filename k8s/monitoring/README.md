# Healthcare Chatbot Monitoring with Loki and Grafana

## Overview

This directory contains the Kubernetes manifests for setting up a modern monitoring stack using Loki and Grafana for the Healthcare Chatbot application. This monitoring solution replaces the previous ELK stack and provides a more resource-efficient way to collect, store, and visualize logs.

## Components

1. **Loki**: A horizontally-scalable, highly-available log aggregation system
2. **Grafana**: A visualization and analytics platform for logs and metrics
3. **Promtail**: A log collector that discovers targets, attaches labels to log streams, and pushes them to Loki

## Deployment Instructions

### Prerequisites

- Kubernetes cluster with sufficient resources
- kubectl configured to communicate with your cluster
- Healthcare Chatbot application deployed

### Step 1: Create the monitoring namespace

```bash
kubectl create namespace monitoring
```

### Step 2: Deploy RBAC resources for Promtail

```bash
kubectl apply -f promtail-rbac.yaml
```

### Step 3: Deploy Loki

```bash
kubectl apply -f loki-config.yaml
kubectl apply -f loki-deployment.yaml
```

### Step 4: Deploy Grafana

```bash
kubectl apply -f grafana-datasources.yaml
kubectl apply -f grafana-deployment.yaml
```

### Step 5: Deploy Promtail

```bash
kubectl apply -f promtail-config.yaml
kubectl apply -f promtail-daemonset.yaml
```

### Step 6: Update the Healthcare Chatbot monitoring module

```bash
kubectl apply -f monitoring-module-configmap.yaml
```

### Step 7: Deploy the Healthcare Chatbot with optimized resources

```bash
kubectl apply -f ../healthcare-chatbot-optimized.yaml
```

## Accessing the Monitoring Stack

### Grafana Dashboard

Set up port forwarding to access the Grafana dashboard:

```bash
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```

Then open a browser and navigate to http://localhost:3000. The default login credentials are:
- Username: admin
- Password: admin

### Healthcare Chatbot

Set up port forwarding to access the Healthcare Chatbot:

```bash
kubectl port-forward svc/healthcare-chatbot 3001:3000 -n healthcare-chatbot
```

Then open a browser and navigate to http://localhost:3001.

## Resource Requirements

Based on testing, here are the recommended resource requirements:

1. **Healthcare Chatbot**:
   - Memory: 2Gi (limit), 1Gi (request)
   - CPU: 500m (limit), 250m (request)

2. **Loki**:
   - Memory: 1Gi (limit), 256Mi (request)
   - CPU: 500m (limit), 100m (request)

3. **Grafana**:
   - Memory: 1Gi (limit), 256Mi (request)
   - CPU: 500m (limit), 100m (request)

4. **Promtail**:
   - Memory: 256Mi (limit), 128Mi (request)
   - CPU: 200m (limit), 100m (request)

## Troubleshooting

### Common Issues

1. **Healthcare Chatbot pod in Pending state**:
   - Check if there are sufficient resources in the cluster
   - Adjust resource limits if necessary
   - Scale down other components temporarily

2. **Healthcare Chatbot pod in CrashLoopBackOff state**:
   - Check logs with `kubectl logs <pod-name> -n healthcare-chatbot`
   - Ensure the monitoring module is correctly mounted
   - Verify that the ConfigMaps are properly created

3. **Logs not appearing in Grafana**:
   - Check if Promtail is running correctly
   - Verify that the Healthcare Chatbot is generating logs
   - Check Loki's status and connectivity

## Customizing Grafana Dashboards

Once you have access to Grafana, you can create custom dashboards for monitoring the Healthcare Chatbot:

1. Click on "+" icon in the left sidebar and select "Dashboard"
2. Click "Add new panel"
3. Select "Loki" as the data source
4. Use the following LogQL query to get started:
   ```
   {app="healthcare-chatbot"}
   ```
5. Customize the visualization as needed
6. Save the dashboard

## Cleaning Up

To remove the monitoring stack:

```bash
kubectl delete -f promtail-daemonset.yaml
kubectl delete -f grafana-deployment.yaml
kubectl delete -f loki-deployment.yaml
kubectl delete -f promtail-config.yaml
kubectl delete -f grafana-datasources.yaml
kubectl delete -f loki-config.yaml
kubectl delete -f promtail-rbac.yaml
kubectl delete namespace monitoring
```
