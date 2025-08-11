#!/bin/bash
set -e

echo "🚀 TruCtrl Deployment Script"
echo "=============================="

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl is not installed. Please install it first:"
    echo "   brew install doctl"
    echo "   or visit: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if user is authenticated with doctl
if ! doctl account get &> /dev/null; then
    echo "❌ Not authenticated with Digital Ocean."
    echo "   Please run: doctl auth init"
    exit 1
fi

echo "✅ doctl is installed and authenticated"

# Build and test locally first
echo "🔨 Building Docker image locally for testing..."
docker build -t tructrl-api .

echo "🧪 Testing the Docker container..."
docker run --rm -d --name tructrl-test -p 8001:8000 tructrl-api
sleep 10

# Test health endpoint
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
    docker stop tructrl-test
else
    echo "❌ Health check failed"
    docker stop tructrl-test || true
    exit 1
fi

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo "❌ This is not a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin <your-repo-url>"
    echo "   git push -u origin main"
    exit 1
fi

echo "📝 Please ensure your code is pushed to GitHub first."
echo "   Then update the .do/app.yaml file with your GitHub repository URL."
echo ""
echo "To deploy to Digital Ocean App Platform:"
echo "1. Go to https://cloud.digitalocean.com/apps"
echo "2. Click 'Create App'"
echo "3. Choose 'GitHub' as source"
echo "4. Select your repository"
echo "5. Upload the .do/app.yaml specification file"
echo "6. Review and deploy"
echo ""
echo "Alternatively, you can use doctl:"
echo "   doctl apps create .do/app.yaml"
echo ""
echo "✅ Pre-deployment checks completed successfully!"
