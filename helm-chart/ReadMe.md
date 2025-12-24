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
| `image.flask.repository` | Flask image repository | `luciancibu/flask-counter` |
| `image.flask.tag` | Flask image tag | `"1.0"` |
| `image.nginx.repository` | Nginx image repository | `luciancibu/nginx-resume` |
| `image.nginx.tag` | Nginx image tag | `"1.0"` |
| `image.mariadb.repository` | MariaDB image repository | `mariadb` |
| `image.mariadb.tag` | MariaDB image tag | `"10.11"` |
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
ingress:
  host: myapp.example.com
mariadb:
  storage: 5Gi
```

```bash
helm install my-app ./helm-chart -f custom-values.yaml
```