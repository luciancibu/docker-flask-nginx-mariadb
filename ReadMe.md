# GitOps Resume Application

A **resume website** built with **Flask**, **Nginx**, and **MariaDB**, featuring automated CI/CD pipelines and deployments to both **AWS EKS** and **Kubernetes (kOps)**. 

## Architecture

```
User Browser
   |
   v
AWS Load Balancer / Ingress
   |
   v
Nginx Service (ClusterIP)
   |
   |-- /        -> Static Resume HTML (Nginx)
   |-- /view    -> View Counter API (Flask)
   |
   v
Flask Service (ClusterIP)
   |
   v
MariaDB Service (ClusterIP)
   |
   v
MariaDB Pod + PersistentVolume
```

## Features

- **Interactive Resume Website**: Professional resume with real-time view counter
- **Microservices Architecture**: Containerized Flask API, Nginx reverse proxy, MariaDB database
- **Dual CI/CD Pipelines**: 
  - AWS EKS deployment with ECR
  - kOps Kubernetes deployment with Docker Hub
- **Infrastructure as Code**: Helm charts and Kubernetes manifests
- **Automated Testing**: Unit tests, code quality checks (flake8, pylint)
- **Production Ready**: Health checks, persistent storage, ingress configuration

##  Project Structure

```
.
├── .github/workflows/
│   ├── main.yml              # AWS EKS CI/CD pipeline
│   └── kops-ci-cd.yaml       # kOps Kubernetes CI/CD pipeline
├── app/
│   ├── flask/
│   │   ├── app.py            # Flask API with view counter
│   │   ├── Dockerfile        # Flask container
│   │   ├── requirements.txt  # Python dependencies
│   │   └── test_app.py       # API tests
│   ├── nginx/
│   │   ├── html/
│   │   │   ├── index.html    # Resume website
│   │   │   └── style.css     # Styling
│   │   ├── default.conf      # Nginx configuration
│   │   └── Dockerfile        # Nginx container
│   ├── mariadb/
│   │   ├── Dockerfile        # MariaDB container
│   │   └── init.sql          # Database initialization
│   └── docker-compose.yml    # Local development setup
├── helm-chart/
│   ├── templates/            # Kubernetes manifests
│   ├── Chart.yaml           # Helm chart metadata
│   ├── values.yaml          # Default configuration
│   └── ReadMe.md            # Helm deployment guide
├── kubedefs/                # Raw Kubernetes manifests
└── kopscreate.md           # kOps cluster setup guide
```

## Services

### Nginx
- Serves static resume website (`index.html`)
- Reverse proxy for Flask API
- Routes:
  - `/` → Resume website with CSS styling
  - `/view` → Flask view counter API

### Flask API
- RESTful API with view counter functionality
- Endpoints:
  - `GET /view` → Increment and return view count
  - `GET /view?read=true` → Return view count (read-only)
- Database connection with retry logic
- Environment-based configuration

### MariaDB
- Persistent database for view counter storage
- Automatic table initialization
- Kubernetes PersistentVolume for data persistence

##  Deployment Options

### Option 1: AWS EKS (Recommended)

**Prerequisites:**
- AWS Account with EKS cluster
- ECR repositories: `resume-flask`, `resume-nginx`
- GitHub Secrets configured

**Automatic Deployment:**
```bash
# Push to main branch triggers automatic deployment
git push origin main
```

**Manual Deployment:**
```bash
# Configure AWS CLI
aws configure

# Deploy with Helm
helm upgrade --install flask-nginx-mariadb ./helm-chart \
  --set image.flask.repository=YOUR_ACCOUNT.dkr.ecr.us-east-2.amazonaws.com/resume-flask \
  --set image.flask.tag=latest \
  --set image.nginx.repository=YOUR_ACCOUNT.dkr.ecr.us-east-2.amazonaws.com/resume-nginx \
  --set image.nginx.tag=latest
```

### Option 2: kOps Kubernetes

**Prerequisites:**
- kOps cluster (see `kopscreate.md`)
- Docker Hub account
- GitHub Secrets configured

**Deployment:**
```bash
# Trigger workflow manually or push to main
# Images will be built and pushed to Docker Hub
# Kubernetes deployments will be updated automatically
```

### Option 3: Local Development

```bash
# Start all services
cd app
docker-compose up -d --build

# Access application
open http://localhost

# Run tests
cd flask
python test_app.py

# Stop services
docker-compose down
```

##  Configuration

### Environment Variables (Flask)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password  
- `DB_HOST`: Database hostname
- `DB_PORT`: Database port (default: 3306)
- `DB_NAME`: Database name

### Helm Values
Key configuration options in `helm-chart/values.yaml`:
- `replicaCount`: Number of replicas per service
- `image`: Container image repositories and tags
- `mariadb`: Database configuration and storage
- `ingress`: Domain and SSL configuration

##  Testing & Quality

### Automated Testing
- **Unit Tests**: Flask API functionality testing
- **Integration Tests**: Docker Compose service testing
- **Code Quality**: flake8 linting, pylint static analysis
- **Security**: Container scanning (optional SonarCloud integration)

### Manual Testing
```bash
# Test view counter API
curl http://your-domain/view
curl http://your-domain/view?read=true

# Check service health
kubectl get pods
kubectl logs deployment/flask-nginx-mariadb-flask
```

## CI/CD Pipelines

### AWS EKS Pipeline (`main.yml`)
1. **Testing**: Unit tests, code quality checks
2. **Build & Publish**: Docker images to ECR
3. **Deploy**: Helm deployment to EKS

### kOps Pipeline (`kops-ci-cd.yaml`)  
1. **Build & Publish**: Docker images to Docker Hub
2. **Deploy**: Update Kubernetes deployments

## Monitoring & Troubleshooting

### Useful Commands
```bash
# Check deployment status
kubectl get pods,svc,pvc
helm status flask-nginx-mariadb

# View logs
kubectl logs deployment/flask-nginx-mariadb-flask
kubectl logs deployment/flask-nginx-mariadb-nginx
kubectl logs deployment/flask-nginx-mariadb-mariadb

# Debug connectivity
kubectl exec -it deployment/flask-nginx-mariadb-nginx -- sh
curl http://flask-nginx-mariadb-flask:5000/view
```

### Common Issues
- **Database Connection**: Check MariaDB pod logs and service endpoints
- **Image Pull**: Verify ECR/Docker Hub credentials and image tags
- **Ingress**: Ensure ingress controller is installed and configured

##  Cleanup

### Helm Deployment
```bash
helm uninstall flask-nginx-mariadb
kubectl delete pvc flask-nginx-mariadb-pvc
```

### Local Development
```bash
cd app
docker-compose down -v
docker system prune
```