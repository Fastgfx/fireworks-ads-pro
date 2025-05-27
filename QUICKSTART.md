# Quick Setup Instructions

## Download and Setup

1. **Download the package**: `fireworks-ads-pro.tar.gz`
2. **Extract**: `tar -xzf fireworks-ads-pro.tar.gz`
3. **Navigate**: `cd fireworks-ads-pro`

## Environment Files

Create these .env files with your own configurations:

### backend/.env
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=fireworks_advertising
JWT_SECRET=your-super-secure-jwt-secret-change-this-123456789
```

### frontend/.env
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Quick Start Commands

### Terminal 1 - Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

### Terminal 2 - Frontend
```bash
cd frontend
yarn install
yarn start
```

## What You'll Need

- **Python 3.8+**
- **Node.js 16+** 
- **Yarn** (`npm install -g yarn`)
- **MongoDB** (local or cloud)

## Live Demo

Your app will run at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001

## Key Features Working

✅ **Product Catalog** - 6 different advertising products
✅ **Logo Upload & Positioning** - Click to position logos on products  
✅ **User Accounts** - Registration/login with wholesale options
✅ **Real-time Preview** - See customizations instantly
✅ **Quote System** - Request pricing for customized products
✅ **Wholesale Pricing** - Different rates for approved accounts

## Adding Stripe Later

When ready for payments:
1. Get Stripe API keys
2. Contact developer for integration
3. Test in sandbox first

## Need Help?

- Check README.md for detailed instructions
- All code is well-commented
- MongoDB will auto-create collections
- Environment variables are clearly marked

**Ready to launch your fireworks advertising business!** 🎆