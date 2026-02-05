# PM Analytics - GitHub Pages Deployment Guide

This guide walks you through deploying PM Analytics to GitHub Pages with automatic CI/CD using GitHub Actions.

## 🎯 Overview

PM Analytics is configured to automatically deploy to GitHub Pages whenever you push changes to the `main` branch. The deployment uses Next.js static export to generate a fully static website.

## ✅ Prerequisites

Before deploying, ensure you have:

1. A GitHub account
2. Git installed on your local machine
3. Node.js 18+ and npm installed (for local development)
4. The PM Analytics repository cloned locally

## 🚀 Quick Start Deployment

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. In the left sidebar, click **Pages**
4. Under "Build and deployment":
   - **Source**: Select **GitHub Actions** (not "Deploy from a branch")
5. Save the settings

### Step 2: Push to GitHub

If you haven't already pushed the code to GitHub:

```bash
# Navigate to the project directory
cd "/Users/marcushudson/Desktop/PMA/PM Analytics"

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit the changes
git commit -m "Initial commit: PM Analytics with GitHub Pages deployment"

# Add remote repository (replace with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/PM-Analytics.git

# Push to GitHub
git push -u origin main
```

### Step 3: Monitor Deployment

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. You should see a workflow called "Deploy PM Analytics to GitHub Pages" running
4. Click on the workflow to see the build and deployment progress
5. Once completed (green checkmark), your site is live!

### Step 4: Access Your Site

Your PM Analytics dashboard will be available at:
```
https://YOUR_USERNAME.github.io/PM-Analytics/
```

Replace `YOUR_USERNAME` with your GitHub username.

## 🔧 Configuration Details

### Next.js Configuration

The `frontend/next.config.js` file is configured for GitHub Pages:

```javascript
const nextConfig = {
  output: 'export',  // Generate static HTML/CSS/JS
  basePath: '/PM-Analytics',  // Your repository name
  images: {
    unoptimized: true,  // Required for static export
  },
  trailingSlash: true,  // Ensures proper routing
}
```

### GitHub Actions Workflow

The `.github/workflows/deploy.yml` file automates the deployment:

- **Triggers**: Runs on push to `main` branch or manual trigger
- **Build**: Installs dependencies, builds Next.js app, generates static files
- **Deploy**: Uploads and deploys the `out` directory to GitHub Pages

### Key Files

- `.github/workflows/deploy.yml` - GitHub Actions deployment workflow
- `frontend/next.config.js` - Next.js configuration for static export
- `frontend/public/.nojekyll` - Prevents Jekyll processing on GitHub Pages

## 🛠️ Local Development

Before deploying, test the build locally:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Run development server
npm run dev
# Visit: http://localhost:3000

# Build for production
npm run build
# Static files will be in the 'out' directory
```

## 🔄 Updating Your Site

To update your deployed site:

1. Make changes to your code
2. Test locally with `npm run dev`
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
4. GitHub Actions will automatically rebuild and deploy

## 🐛 Troubleshooting

### Deployment fails with "Permission denied"

**Solution**: Update repository permissions
1. Go to Settings → Actions → General
2. Under "Workflow permissions", select "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"
4. Save and re-run the workflow

### Site shows 404 error

**Solution**: Verify GitHub Pages settings
1. Go to Settings → Pages
2. Ensure Source is set to "GitHub Actions"
3. Check that the workflow completed successfully (green checkmark in Actions tab)
4. Wait a few minutes for DNS propagation

### Assets not loading (CSS/JS/images)

**Solution**: Check basePath configuration
1. Verify `basePath` in `next.config.js` matches your repository name
2. Repository name is case-sensitive: `PM-Analytics` not `pm-analytics`
3. Rebuild and redeploy

### Build fails during npm install

**Solution**: Check Node.js version
1. Ensure you're using Node.js 18 or higher
2. Delete `node_modules` and `package-lock.json`
3. Run `npm install` again
4. Commit the new `package-lock.json`

## 📊 Monitoring

### View Deployment Status

1. **Actions Tab**: Shows all workflow runs and their status
2. **Deployments**: In the right sidebar, shows active deployments
3. **Pages Settings**: Shows the current live URL

### Deployment Logs

To view detailed logs:
1. Go to Actions tab
2. Click on the workflow run
3. Click on "build" or "deploy" to see step-by-step logs

## 🔒 Security Considerations

- All data in the MVP is static mock data (no backend)
- No sensitive information is exposed
- HTTPS is automatically enabled by GitHub Pages
- No API keys or credentials are required for the static site

## 🎨 Customization

### Changing the Repository Name

If you rename your repository, update:

1. `frontend/next.config.js` - Update `basePath` value
2. `frontend/README.md` - Update the live demo URL
3. Push changes to GitHub
4. The site will be at: `https://YOUR_USERNAME.github.io/NEW-NAME/`

### Custom Domain

To use a custom domain (e.g., `analytics.yourdomain.com`):

1. Go to Settings → Pages
2. Under "Custom domain", enter your domain
3. Add DNS records at your domain provider:
   - Type: CNAME
   - Name: analytics (or your subdomain)
   - Value: YOUR_USERNAME.github.io
4. Update `next.config.js` to remove or adjust `basePath`

## 📝 Next Steps

1. ✅ Deploy to GitHub Pages (you're here!)
2. ⬜ Share the live URL with stakeholders
3. ⬜ Collect feedback on the MVP
4. ⬜ Add real data integration (future phase)
5. ⬜ Connect to backend API (future phase)

## 🤝 Support

For issues or questions:
- Check the troubleshooting section above
- Review GitHub Actions logs for error details
- Verify all configuration files match this guide

## 📚 Resources

- [Next.js Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Last Updated**: February 5, 2026
