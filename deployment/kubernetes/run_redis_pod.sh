#!/bin/bash


# Following is just to demo that the kubernetes cluster works.
kubectl cluster-info
# Wait for kube-dns to be ready.
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl -n kube-system get pods -lk8s-app=kube-dns -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True";
do
    sleep 1
    echo "waiting for kube-dns to be available"
    kubectl get pods --all-namespaces
done
# Create example Redis deployment on Kubernetes.
kubectl run travis-example --image=redis --labels="app=travis-example"
# Make sure created pod is scheduled and running.
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl -n default get pods -lapp=travis-example -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"
do
    sleep 1
    echo "waiting for travis-example deployment to be available"
    kubectl get pods -n default
done