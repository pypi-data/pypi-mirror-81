#!/bin/bash
kubectl delete namespaces $3 --wait=true --timeout=15m || :
kubectl create ns $3
kubectl create secret generic \
  azure-secret --from-literal=azurestorageaccountname=$1 \
  --from-literal=azurestorageaccountkey=$2 -n $3
