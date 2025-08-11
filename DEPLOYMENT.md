# TruCtrl Deployment Guide

This guide covers deploying the TruCtrl API to Digital Ocean App Platform.

## Prerequisites

1. **Digital Ocean Account**: Create an account at [digitalocean.com](https://digitalocean.com)
2. **GitHub Repository**: Your code must be in a GitHub repository
3. **doctl CLI** (optional): Install for command-line deployment
   ```bash
   # macOS
   brew install doctl
   
   # Authenticate
   doctl auth init
   ```

## Quick Deployment

### Option 1: Using Digital Ocean Dashboard (Recommended)

1. Push your code to GitHub
2. Go to [Digital Ocean App Platform](https://cloud.digitalocean.com/apps)
3. Click **"Create App"**
4. Select **"GitHub"** as source
5. Choose your repository and branch
6. Upload the `.do/app.yaml` specification file
7. Review settings and click **"Create Resources"**

### Option 2: Using Command Line

1. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

2. If all checks pass, deploy with doctl:
   ```bash
   doctl apps create .do/app.yaml
   ```

## Configuration

### Environment Variables

The app will automatically use these environment variables:

- `DATABASE_URL`: SQLite database path (default: `sqlite:///app/data/tructrl.db`)
- `PYTHONPATH`: Python path (set to `/app`)
- `PORT`: Application port (set by App Platform)

### Custom Domain (Optional)

After deployment:
1. Go to your app in the Digital Ocean dashboard
2. Navigate to **Settings** > **Domains**
3. Add your custom domain
4. Update DNS records as instructed

## Database Setup

The app uses SQLite by default, which is suitable for small to medium applications. The database will be automatically created and migrated on first run.

### Upgrading to PostgreSQL (Recommended for Production)

1. Create a PostgreSQL database in Digital Ocean:
   ```bash
   doctl databases create tructrl-db --engine postgres --size db-s-1vcpu-1gb
   ```

2. Update your app's environment variables:
   - `DATABASE_URL`: Use the connection string from your database

3. Redeploy the application

## Monitoring and Logs

- **Logs**: View in Digital Ocean dashboard under your app > **Runtime Logs**
- **Metrics**: Monitor performance in the **Insights** tab
- **Health Check**: The app includes a `/health` endpoint for monitoring

## Scaling

The app is configured with:
- **Instance Size**: `basic-xxs` (cheapest option)
- **Instance Count**: `1`

To scale up:
1. Go to your app settings
2. Update instance size or count
3. Apply changes

## Cost Estimates

- **Basic XXS**: ~$5/month for the API
- **PostgreSQL**: ~$15/month (optional)
- **Bandwidth**: Usually within free tier limits

## Security Notes

1. **Environment Variables**: Never commit `.env` files
2. **Secret Keys**: Generate unique secret keys for production
3. **CORS**: Update allowed origins for your frontend domain
4. **HTTPS**: Automatically provided by App Platform

## Troubleshooting

### Build Failures
- Check build logs in the Digital Ocean dashboard
- Ensure all dependencies are in `pyproject.toml`
- Verify Python version compatibility

### Runtime Errors
- Check application logs
- Verify environment variables
- Test health endpoint: `https://your-app-url/health`

### Database Issues
- Check database migrations ran successfully
- Verify database permissions
- Review database connection string

## Support

For issues:
1. Check the [Digital Ocean App Platform docs](https://docs.digitalocean.com/products/app-platform/)
2. Review application logs
3. Test locally with Docker: `docker-compose up`
