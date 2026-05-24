# VM Hosting Terraform

This Terraform tree provisions only the **application hosting runtime** for the Azure-Native Kubernetes Environment Governance & Resource Optimization Platform.

It intentionally does **not** provision:

- AKS clusters
- Kubernetes resources
- databases
- Container Apps
- App Service
- monitoring stacks

AKS environments are expected to live in a separate infrastructure repository. This VM exists so Phase 1 has professional public URLs, SSL termination, and a stable runtime for the Next.js frontend, FastAPI backend, Nginx, Docker, Azure CLI, and AKS governance services.

## Architecture

```text
Internet
  |
Azure Static Public IP
  |
NSG: 22, 80, 443
  |
Ubuntu 22.04 VM
  |
Nginx reverse proxy + Let's Encrypt
  |
+----------------------+----------------------+
| governance.vaultrix.in        api.governance.vaultrix.in |
| Next.js frontend :3000        FastAPI backend :8000      |
+----------------------+----------------------+
```

The VM can use a system-assigned managed identity. Assign Azure RBAC roles to that identity so the backend can discover AKS clusters and query Azure APIs without storing Azure credentials on the VM.

Recommended roles for the VM managed identity, scoped as narrowly as possible:

- Reader
- Azure Kubernetes Service Cluster User Role
- Monitoring Reader

## Folder Structure

```text
terraform/vm-hosting/
  environments/dev/
    main.tf
    variables.tf
    outputs.tf
    providers.tf
    terraform.tfvars.example
    backend.tf.example
  modules/
    network/
    public_ip/
    security/
    vm/
  scripts/bootstrap.sh
```

## Prerequisites

- Terraform >= 1.7
- Azure CLI authenticated to the target subscription
- An SSH key pair
- Permission to create Azure networking, public IP, and VM resources

Create an SSH key if needed:

```bash
ssh-keygen -t ed25519 -C "aks-governance-vm" -f ~/.ssh/aks_governance_vm
```

On Windows PowerShell:

```powershell
ssh-keygen -t ed25519 -C "aks-governance-vm" -f $env:USERPROFILE\.ssh\aks_governance_vm
```

## Configure Terraform

```bash
cd terraform/vm-hosting/environments/dev
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
resource_group_name = "rg-aks-governance-host-dev"
location            = "centralindia"
name_prefix         = "aks-gov"
vm_name             = "aks-gov-host-dev"
vm_size             = "Standard_B2s"
admin_username      = "azureuser"
ssh_public_key_path = "~/.ssh/aks_governance_vm.pub"

allowed_ssh_source_cidrs = ["YOUR_PUBLIC_IP/32"]
```

For a pitch, restrict SSH to your current public IP. Avoid leaving SSH open to `0.0.0.0/0` unless this is a temporary emergency.

## Terraform Init, Plan, Apply

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

After apply, Terraform outputs:

- VM public IP
- SSH command
- resource group name
- VM name
- recommended DNS records
- VM managed identity principal id

## SSH Access

Use the output command:

```bash
ssh azureuser@<VM_PUBLIC_IP>
```

If you used a non-default private key:

```bash
ssh -i ~/.ssh/aks_governance_vm azureuser@<VM_PUBLIC_IP>
```

## DNS Configuration In GoDaddy

Create two **A records** pointing to the Terraform output `vm_public_ip`.

| Type | Name | Value |
| --- | --- | --- |
| A | `governance` | `<VM_PUBLIC_IP>` |
| A | `api.governance` | `<VM_PUBLIC_IP>` |

This creates:

```text
governance.vaultrix.in
api.governance.vaultrix.in
```

Use A records because this Terraform creates a static public IP. If you later move to Azure Container Apps or Front Door, use CNAME records to the Azure-provided hostname instead.

DNS may take several minutes to propagate. Verify:

```bash
nslookup governance.vaultrix.in
nslookup api.governance.vaultrix.in
```

## VM Bootstrap

The VM bootstrap script installs:

- Docker Engine
- Docker Compose plugin
- Nginx
- Certbot
- Python 3
- Node.js LTS
- Azure CLI
- Git, jq, unzip

The script also prepares:

```text
/opt/aks-governance/frontend
/opt/aks-governance/backend
/opt/aks-governance/deploy
/opt/aks-governance/logs
```

## Docker Deployment Pattern

Build and run the frontend/backend using Docker Compose or direct Docker commands.

Example deployment layout on the VM:

```text
/opt/aks-governance/deploy/docker-compose.yml
/opt/aks-governance/deploy/.env
```

Recommended container ports:

```text
frontend: 127.0.0.1:3000
backend:  127.0.0.1:8000
```

Keep application containers bound to localhost and expose only Nginx publicly on ports 80/443.

## Nginx Reverse Proxy

Create:

```bash
sudo nano /etc/nginx/sites-available/aks-governance
```

Use this HTTP-first config before issuing certificates:

```nginx
server {
    listen 80;
    server_name governance.vaultrix.in;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name api.governance.vaultrix.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/aks-governance /etc/nginx/sites-enabled/aks-governance
sudo nginx -t
sudo systemctl reload nginx
```

## SSL With Let's Encrypt

After DNS points to the VM public IP and Nginx responds on HTTP:

```bash
sudo certbot --nginx \
  -d governance.vaultrix.in \
  -d api.governance.vaultrix.in
```

Choose the HTTPS redirect option when prompted.

Verify auto-renewal:

```bash
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

## Entra ID Redirect URIs

Once SSL is working, configure Microsoft Entra:

Frontend SPA redirect URI:

```text
https://governance.vaultrix.in/auth/callback
```

Frontend environment:

```env
NEXT_PUBLIC_API_BASE_URL=https://api.governance.vaultrix.in/api/v1
NEXT_PUBLIC_AZURE_REDIRECT_URI=https://governance.vaultrix.in/auth/callback
```

Backend environment:

```env
BACKEND_CORS_ORIGINS=https://governance.vaultrix.in
```

## Future Migration

This VM-first design is for Phase 1 pitching and public URL readiness. Later phases can migrate runtime hosting to:

- Azure Container Apps
- Azure App Service
- AKS-hosted application runtime
- Azure Front Door in front of any of the above

The domain strategy can remain stable while the backend target changes.

