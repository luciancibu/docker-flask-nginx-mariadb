# Flask + Nginx + MariaDB Helm Chart

## Prerequisites

### Install Helm

**Windows:**
```bash
# Using Chocolatey
choco install kubernetes-helm

# Using Scoop
scoop install helm

# Manual download
# Download from https://github.com/helm/helm/releases
# Extract and add to PATH
```

**Linux:**
```bash
# Using package manager
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm

# Using snap
sudo snap install helm --classic
```

### Verify Installation
```bash
helm version
```

### Install Metrics Server (for HPA)
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Quick Start

```bash
# Install
helm install my-app ./helm-chart

# Upgrade
helm upgrade my-app ./helm-chart

# Uninstall
helm uninstall my-app
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `name` | Application name | `flask-nginx-mariadb` |
| `replicaCount.flask` | Number of Flask replicas | `2` |
| `replicaCount.nginx` | Number of Nginx replicas | `2` |
| `image.flask.repository` | Flask image repository | `""` |
| `image.flask.tag` | Flask image tag | `""` |
| `image.nginx.repository` | Nginx image repository | `""` |
| `image.nginx.tag` | Nginx image tag | `""` |
| `image.mariadb.repository` | MariaDB image repository | `mariadb` |
| `image.mariadb.tag` | MariaDB image tag | `"10.11"` |
| `resources.flask.requests.cpu` | Flask CPU requests | `100m` |
| `resources.flask.requests.memory` | Flask memory requests | `128Mi` |
| `resources.flask.limits.cpu` | Flask CPU limits | `300m` |
| `resources.flask.limits.memory` | Flask memory limits | `256Mi` |
| `resources.nginx.requests.cpu` | Nginx CPU requests | `50m` |
| `resources.nginx.requests.memory` | Nginx memory requests | `64Mi` |
| `resources.nginx.limits.cpu` | Nginx CPU limits | `150m` |
| `resources.nginx.limits.memory` | Nginx memory limits | `128Mi` |
| `autoscaling.flask.enabled` | Enable Flask HPA | `true` |
| `autoscaling.flask.minReplicas` | Flask min replicas | `2` |
| `autoscaling.flask.maxReplicas` | Flask max replicas | `4` |
| `autoscaling.flask.targetCPUUtilizationPercentage` | Flask CPU target | `70` |
| `autoscaling.flask.targetMemoryUtilizationPercentage` | Flask memory target | `80` |
| `autoscaling.nginx.enabled` | Enable Nginx HPA | `true` |
| `autoscaling.nginx.minReplicas` | Nginx min replicas | `2` |
| `autoscaling.nginx.maxReplicas` | Nginx max replicas | `4` |
| `autoscaling.nginx.targetCPUUtilizationPercentage` | Nginx CPU target | `70` |
| `autoscaling.nginx.targetMemoryUtilizationPercentage` | Nginx memory target | `80` |
| `mariadb.rootPassword` | MariaDB root password | `rootpass` |
| `mariadb.database` | Database name | `cv` |
| `mariadb.user` | Database user | `cvuser` |
| `mariadb.password` | Database password | `cvpass` |
| `mariadb.storage` | Storage size | `3Gi` |
| `mariadb.storageClassName` | Storage class | `default` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class | `nginx` |
| `ingress.host` | Ingress hostname | `resume.kakosnita.xyz` |
| `service.type` | Service type | `ClusterIP` |
| `service.nginx.port` | Nginx service port | `80` |
| `service.flask.port` | Flask service port | `5000` |
| `service.mariadb.port` | MariaDB service port | `3306` |

## Custom Values

```bash
helm install my-app ./helm-chart --set ingress.host=myapp.example.com
```

Or create a custom values file:

```yaml
# custom-values.yaml
replicaCount:
  flask: 3
  nginx: 3
autoscaling:
  flask:
    maxReplicas: 6
  nginx:
    maxReplicas: 6
ingress:
  host: myapp.example.com
mariadb:
  storage: 5Gi
```

```bash
helm install my-app ./helm-chart -f custom-values.yaml
```

## Monitoring Autoscaling

```bash
# Check HPA status
kubectl get hpa

# View detailed HPA info
kubectl describe hpa flask-nginx-mariadb-flask-hpa
kubectl describe hpa flask-nginx-mariadb-nginx-hpa
```

## Notes

- **Resource limits optimized for t3.small EKS nodes**
- **HPA requires metrics-server to be installed**
- **Autoscaling can be disabled by setting `autoscaling.*.enabled: false`**