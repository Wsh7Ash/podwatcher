# Security Notes — podwatcher

## What this does

Podwatcher compares the images running in pods against what a registry resolver reports and reports drift.

## Access considerations

- Reading pod and image information requires access to Kubernetes API credentials or a kubeconfig. Treat those credentials as sensitive.
- Querying a registry may expose which images and tags you are running. Consider whether registry access should be restricted or monitored.

## MVP scope

This MVP uses a local mock resolver and a mock enumeration path. It is not intended to connect to real clusters or registries without additional access controls.

## Operational notes

- Do not run this tool with broader cluster access than needed for the audit.
- If you extend it to contact real registries, prefer read-only image metadata access and avoid forwarding credentials.
