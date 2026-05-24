# Deployment

## Mode A: AKS

1. Provision Azure infrastructure:

```powershell
cd infra/terraform/environments/dev
terraform init
terraform plan
terraform apply
```

2. Build and push images to ACR.

3. Deploy with Helm:

```powershell
helm upgrade --install aks-governance ../../helm/aks-governance `
  --namespace aks-governance `
  --create-namespace `
  --set frontend.image.repository=<acr>/aks-governance-frontend `
  --set backend.image.repository=<acr>/aks-governance-api
```

4. Store production secrets in Key Vault and inject them through workload identity or a secrets operator.

## Mode B: Azure Container Apps

The Terraform `container-apps` module currently creates the managed environment foundation. Add app resources, identities, ACR pulls, and Key Vault references in the next increment.

## Security Notes

- Never commit `.env` or Terraform variable files.
- Use Microsoft Entra ID app roles for Admin, Platform Engineer, and Viewer.
- Use least-privilege Azure role assignments for Resource Graph, AKS read access, Monitor read access, ACR pull, and Key Vault secret access.

