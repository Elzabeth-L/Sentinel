#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

log() {
  echo "[$(date --iso-8601=seconds)] $*"
}

log "Updating package index"
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release software-properties-common apt-transport-https

log "Installing base runtime packages"
apt-get install -y nginx certbot python3-certbot-nginx python3 python3-pip python3-venv unzip jq git

log "Installing Docker Engine"
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable --now docker

log "Installing Node.js LTS"
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt-get install -y nodejs

log "Installing Azure CLI"
curl -sL https://aka.ms/InstallAzureCLIDeb | bash

log "Preparing application directories"
mkdir -p /opt/aks-governance/{frontend,backend,deploy,logs}
chown -R "${SUDO_USER:-root}:${SUDO_USER:-root}" /opt/aks-governance || true

log "Writing default Nginx landing page"
cat >/var/www/html/index.html <<'HTML'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sentinel Host</title>
    <style>
      body { margin: 0; font-family: system-ui, -apple-system, Segoe UI, sans-serif; background: #f6f8fb; color: #142033; }
      main { max-width: 760px; margin: 12vh auto; padding: 32px; background: #fff; border: 1px solid #dbe3ee; border-radius: 8px; }
      h1 { margin: 0 0 12px; font-size: 28px; }
      p { line-height: 1.55; color: #64748b; }
      code { background: #eef2f7; padding: 2px 5px; border-radius: 4px; }
    </style>
  </head>
  <body>
    <main>
      <h1>Sentinel host is ready</h1>
      <p>Nginx, Docker, Node.js, Python, Certbot, and Azure CLI are installed. Deploy the frontend/backend services and configure virtual hosts for <code>sentinel.vaultrix.in</code> and <code>api.sentinel.vaultrix.in</code>.</p>
    </main>
  </body>
</html>
HTML

nginx -t
systemctl enable --now nginx

log "Bootstrap complete"
