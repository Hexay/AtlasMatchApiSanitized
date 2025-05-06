# Quick Deployment Guide

## 1. Server Setup
- Get a Linux server (Ubuntu recommended)
- Point your domain to the server's IP
- Install Docker & Docker Compose:
```bash
curl -fsSL https://get.docker.com | sh
sudo apt install docker-compose git
```

## 2. Get Code
```bash
# Clone the repository
git clone https://github.com/your-username/MatchApiSanitized.git
cd MatchApiSanitized

# Create your config.json (replace with your tokens)
cat > config.json << EOF
{
    "port": 8001,
    "bm_token": "your-battlemetrics-token-here",
    "api_token": "your-secret-api-token-here"
}
EOF
```

## 3. Configure
Edit `nginx.conf`, replace `your-domain.com` with your actual domain.

## 4. Run
```bash
# Get SSL certificate
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d your-domain.com

# Start everything
docker compose up -d
```

Done! Your API will be available at `https://your-domain.com`

## Common Issues
- Make sure ports 80 and 443 are open
- Check logs: `docker compose logs`
- Restart: `docker compose restart` 