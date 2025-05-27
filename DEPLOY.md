# FireworksAds Pro Deployment Guide

## Quick Deploy Commands

### For GitHub Upload:
```bash
git init
git add .
git commit -m "Initial commit - FireworksAds Pro"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fireworks-ads-pro.git
git push -u origin main
```

### Railway Environment Variables:
```
MONGO_URL=mongodb://mongo:27017/fireworks_advertising
JWT_SECRET=your-super-secure-secret-change-this-12345
PORT=8001
```

### Vercel Environment Variables:
```
REACT_APP_BACKEND_URL=https://your-railway-app.up.railway.app
```

## Deployment Steps:

1. **Create GitHub Repo** - Name it `fireworks-ads-pro`
2. **Upload Code** - Use git commands above
3. **Deploy Backend** - Connect Railway to GitHub repo
4. **Deploy Frontend** - Connect Vercel to GitHub repo  
5. **Configure URLs** - Set environment variables
6. **Test Live Site** - Verify all features work

## Support Links:
- Railway: https://railway.app
- Vercel: https://vercel.com
- MongoDB Atlas: https://cloud.mongodb.com (if needed)