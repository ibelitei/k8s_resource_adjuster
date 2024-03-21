# Kubernetes Resource Adjuster

## Overview

This script dynamically adjusts the resource limits of Kubernetes deployments based on the requested resources. It increases the limits by a user-defined percentage to ensure that the deployments have a buffer above their requested resources, enhancing stability and performance. The script processes a YAML file containing the original resource requests, calculates new limits, and outputs an adjusted YAML file with updated limits and improved readability through added spacing between service definitions.

## Prerequisites

- Python 3.x installed on your machine.
- A YAML file (`original_resources.yaml`) containing the original resource requests for your Kubernetes deployments.

## Installation

No installation is necessary for this script. However, you must have Python 3.x installed on your system. You can download and install Python from [python.org](https://www.python.org/downloads/).

## Configuration

Before running the script, ensure you have your Kubernetes resource request file named `original_resources.yaml` in the same directory as the script. This file should follow the structure as shown in the example below:

```yaml
services:
  resources:
    service-a:
      limits:
        cpu: 200m
        memory: 4Gi
      requests:
        cpu: 100m
        memory: 2Gi
services2:
  resources:
    service-a:
      limits:
        cpu: 200m
        memory: 2Gi
      requests:
        cpu: 100m
        memory: 1Gi
```

## Usage
1. Place your `original_resources.yaml` file in the same directory as the script.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the script.
4. Run the script using Python:

```console
python k8s_resource_adjuster.py
```

When prompted, enter the percentage increase you wish to apply to the resource limits. For example, for a 20% increase, enter 20.

The script will create a new file named `adjusted_resources.yaml` in the same directory, containing the adjusted resource limits.

## Example

Given the ``original original_resources.yaml`` content:

```yaml
services:
  resources:
    service-a:
      limits:
        cpu: 200m
        memory: 4Gi
      requests:
        cpu: 100m
        memory: 2Gi
```

And a specified increase of `20%`, the output will be:

```yaml
services:
  resources:
    service-a:
      limits:
        cpu: 120m
        memory: 2.4Gi
      requests:
        cpu: 100m
        memory: 2Gi
```

