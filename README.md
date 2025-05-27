# FireworksAds Pro - Fireworks Business Advertising Website

A complete web application for fireworks businesses to create custom advertising materials including signs, banners, and flags with logo and text customization.

## 🚀 Features

### Core Functionality
- **Product Catalog**: Feather Flags, Custom Banners, No Smoking Signs
- **Custom Logo Upload**: Support for JPG, PNG, PDF, AI files
- **Logo Positioning**: Click-to-position logos on product previews
- **Text Customization**: Add business name and phone number
- **Real-time Preview**: See customizations live on product images
- **User Accounts**: Registration and login system
- **Wholesale System**: Separate pricing for approved wholesale customers
- **Quote Requests**: Submit customizations for pricing quotes

### User Management
- Regular customer accounts
- Wholesale account applications with approval workflow
- Different pricing tiers based on account type
- User authentication with JWT tokens

## 🛠 Technology Stack

### Frontend
- **React 19** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls

### Backend  
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database for flexible data storage
- **JWT Authentication** - Secure token-based auth
- **File Upload** - Support for logo uploads
- **bcrypt** - Password hashing

## 📋 Prerequisites

Before you begin, ensure you have:
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (v4.4 or higher)
- **Yarn** package manager

## 🔧 Local Development Setup

### 1. Clone/Download the Project
```bash
# Extract the downloaded files to your desired directory
cd fireworks-ads-pro
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB connection string
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Create .env file
cp .env.example .env
# Edit .env with your backend URL
```

### 4. Database Setup
```bash
# Make sure MongoDB is running on your system
# The application will automatically create the necessary collections
```

### 5. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001

## 🌐 Production Deployment

### Environment Variables

**Backend (.env):**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=fireworks_advertising
JWT_SECRET=your-super-secure-jwt-secret-here
```

**Frontend (.env):**
```env
REACT_APP_BACKEND_URL=https://your-api-domain.com
```

### Deployment Options

#### Option 1: Traditional VPS/Server
1. Set up MongoDB on your server
2. Deploy backend with gunicorn/uvicorn
3. Build frontend and serve with nginx
4. Configure SSL certificates

#### Option 2: Cloud Platforms
- **Backend**: Deploy to Heroku, Railway, or DigitalOcean App Platform
- **Frontend**: Deploy to Vercel, Netlify, or similar
- **Database**: Use MongoDB Atlas (cloud)

#### Option 3: Docker (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🔑 Adding Stripe Payment Processing

When you're ready to add payment processing:

1. Sign up for a Stripe account at https://stripe.com
2. Get your API keys from the Stripe dashboard
3. Contact the developer to integrate Stripe using the integration playbook
4. Test with Stripe's test environment before going live

## 📝 Usage Guide

### For Regular Customers
1. **Register** - Create an account with business information
2. **Browse Products** - View available advertising products
3. **Customize** - Select a product and add your logo/text
4. **Position Logo** - Click on the preview to position your logo
5. **Request Quote** - Submit your customization for pricing

### For Wholesale Customers
1. **Register** - Choose "Wholesale Account" during registration
2. **Wait for Approval** - Admin must approve wholesale status
3. **Get Wholesale Pricing** - See discounted prices once approved
4. **Volume Discounts** - Additional discounts based on order volume

### For Administrators
- Approve wholesale accounts through the database
- Manage product catalog
- Review and respond to quote requests

## 🗂 Project Structure

```
fireworks-ads-pro/
├── backend/
│   ├── server.py           # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables
│   └── uploads/           # Uploaded logo files
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styles
│   │   └── index.js       # Entry point
│   ├── package.json       # Node.js dependencies
│   ├── tailwind.config.js # Tailwind configuration
│   └── .env               # Environment variables
└── README.md              # This file
```

## 🔧 Customization

### Adding New Products
Edit the `PRODUCTS` array in `backend/server.py`:

```python
PRODUCTS = [
    {
        "id": "new-product-id",
        "name": "New Product Name",
        "category": "Product Category",
        "description": "Product description",
        "base_price": 99.99,
        "wholesale_price": 79.99,
        "image_url": "https://example.com/image.jpg",
        "customizable": True,
        "sizes": ["Size 1", "Size 2"]
    }
]
```

### Modifying Pricing
- Regular pricing: `base_price` field
- Wholesale pricing: `wholesale_price` field
- Approval logic: `wholesale_approved` field in user accounts

### Styling Changes
- Edit `frontend/src/App.css` for custom styles
- Modify Tailwind classes in `frontend/src/App.js`
- Update colors, fonts, and layout as needed

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check if MongoDB is running
   - Verify Python dependencies are installed
   - Check .env file configuration

2. **Frontend can't connect to backend**
   - Verify REACT_APP_BACKEND_URL in frontend/.env
   - Check if backend is running on correct port
   - Ensure CORS is properly configured

3. **File uploads not working**
   - Check uploads directory permissions
   - Verify file size limits
   - Ensure supported file types

4. **Database connection issues**
   - Verify MongoDB is running
   - Check MONGO_URL in backend/.env
   - Ensure database permissions

## 📞 Support

For technical support or customization requests:
- Review the code comments for implementation details
- Check the API endpoints in `backend/server.py`
- Test API endpoints using the provided testing scripts

## 📄 License

This project is provided as-is for your business use. You have full rights to modify, distribute, and use commercially.

## 🔄 Future Enhancements

Potential features to add:
- Email notifications for quotes
- Admin dashboard for managing orders
- Advanced logo editing tools
- Bulk ordering system
- Customer gallery/portfolio
- Integration with print suppliers
- Mobile app version

---

**Built with ❤️ for Fireworks Businesses**

Need help with setup or customization? The code is well-documented and designed for easy modification.