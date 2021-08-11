#!/bin/bash
set -e
kubectl delete -f dep.yaml
kubectl apply -f dep.yaml