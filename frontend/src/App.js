import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [user, setUser] = useState(null);
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [customization, setCustomization] = useState({
    business_name: '',
    phone_number: '',
    logo_url: null,
    logo_position: { x: 50, y: 50 }
  });
  const [uploadedLogo, setUploadedLogo] = useState(null);
  const [quotes, setQuotes] = useState([]);

  useEffect(() => {
    // Check for existing token
    const token = localStorage.getItem('token');
    if (token) {
      fetchCurrentUser(token);
    }
    fetchProducts();
  }, []);

  const fetchCurrentUser = async (token) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        localStorage.removeItem('token');
      }
    } catch (error) {
      console.error('Error fetching user:', error);
      localStorage.removeItem('token');
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/products`);
      const data = await response.json();
      setProducts(data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchQuotes = async () => {
    if (!user) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/quotes`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setQuotes(data.quotes);
    } catch (error) {
      console.error('Error fetching quotes:', error);
    }
  };

  const handleLogin = async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        setUser(data.user);
        setCurrentView('home');
        return { success: true };
      } else {
        const error = await response.json();
        return { success: false, error: error.detail };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const handleRegister = async (formData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        setUser(data.user);
        setCurrentView('home');
        return { success: true };
      } else {
        const error = await response.json();
        return { success: false, error: error.detail };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setCurrentView('home');
  };

  const handleLogoUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setUploadedLogo(data.file_url);
        setCustomization(prev => ({
          ...prev,
          logo_url: data.file_url
        }));
        return true;
      }
    } catch (error) {
      console.error('Error uploading logo:', error);
    }
    return false;
  };

  const handleRequestQuote = async () => {
    if (!user || !selectedProduct) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/quotes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_email: user.email,
          business_name: customization.business_name,
          product_name: selectedProduct.name,
          customization_data: customization,
          quantity: 1,
          message: `Custom ${selectedProduct.name} with business name: ${customization.business_name}, phone: ${customization.phone_number}`
        })
      });

      if (response.ok) {
        alert('Quote request submitted successfully! We\'ll contact you within 24 hours.');
        setCurrentView('quotes');
        fetchQuotes();
      }
    } catch (error) {
      console.error('Error requesting quote:', error);
    }
  };

  const getPrice = (product) => {
    if (user && user.account_type === 'wholesale' && user.wholesale_approved) {
      return product.wholesale_price;
    }
    return product.base_price;
  };

  const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
      e.preventDefault();
      const result = await handleLogin(email, password);
      if (!result.success) {
        setError(result.error);
      }
    };

    return (
      <div className="auth-container">
        <div className="auth-card">
          <h2>Login to Your Account</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && <div className="error">{error}</div>}
            <button type="submit">Login</button>
          </form>
          <p>
            Don't have an account?{' '}
            <button onClick={() => setCurrentView('register')} className="link-button">
              Register here
            </button>
          </p>
        </div>
      </div>
    );
  };

  const RegisterForm = () => {
    const [formData, setFormData] = useState({
      email: '',
      password: '',
      business_name: '',
      phone: '',
      account_type: 'regular'
    });
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
      e.preventDefault();
      const result = await handleRegister(formData);
      if (!result.success) {
        setError(result.error);
      }
    };

    return (
      <div className="auth-container">
        <div className="auth-card">
          <h2>Create Your Account</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
            <input
              type="text"
              placeholder="Business Name"
              value={formData.business_name}
              onChange={(e) => setFormData({...formData, business_name: e.target.value})}
              required
            />
            <input
              type="tel"
              placeholder="Phone Number"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              required
            />
            <select
              value={formData.account_type}
              onChange={(e) => setFormData({...formData, account_type: e.target.value})}
            >
              <option value="regular">Regular Customer</option>
              <option value="wholesale">Wholesale Account</option>
            </select>
            {formData.account_type === 'wholesale' && (
              <div className="wholesale-notice">
                <p>Wholesale accounts require approval. You'll receive regular pricing until approved.</p>
              </div>
            )}
            {error && <div className="error">{error}</div>}
            <button type="submit">Register</button>
          </form>
          <p>
            Already have an account?{' '}
            <button onClick={() => setCurrentView('login')} className="link-button">
              Login here
            </button>
          </p>
        </div>
      </div>
    );
  };

  const ProductCustomizer = () => {
    const [logoPosition, setLogoPosition] = useState({ x: 50, y: 50 });

    const handleLogoMove = (e) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setLogoPosition({ x, y });
      setCustomization(prev => ({
        ...prev,
        logo_position: { x, y }
      }));
    };

    return (
      <div className="customizer-container">
        <div className="customizer-header">
          <button onClick={() => setCurrentView('products')} className="back-button">
            ← Back to Products
          </button>
          <h2>Customize {selectedProduct.name}</h2>
        </div>

        <div className="customizer-content">
          <div className="product-preview">
            <div className="preview-container" onClick={handleLogoMove}>
              <img src={selectedProduct.image_url} alt={selectedProduct.name} />
              {uploadedLogo && (
                <div
                  className="logo-overlay"
                  style={{
                    left: `${logoPosition.x}%`,
                    top: `${logoPosition.y}%`,
                    transform: 'translate(-50%, -50%)'
                  }}
                >
                  <img src={uploadedLogo} alt="Logo" />
                </div>
              )}
              {customization.business_name && (
                <div className="text-overlay business-name">
                  {customization.business_name}
                </div>
              )}
              {customization.phone_number && (
                <div className="text-overlay phone-number">
                  {customization.phone_number}
                </div>
              )}
            </div>
            <p className="preview-instructions">
              Click on the image to position your logo
            </p>
          </div>

          <div className="customization-panel">
            <div className="customization-section">
              <h3>Text Information</h3>
              <input
                type="text"
                placeholder="Business Name"
                value={customization.business_name}
                onChange={(e) => setCustomization(prev => ({
                  ...prev,
                  business_name: e.target.value
                }))}
              />
              <input
                type="tel"
                placeholder="Phone Number"
                value={customization.phone_number}
                onChange={(e) => setCustomization(prev => ({
                  ...prev,
                  phone_number: e.target.value
                }))}
              />
            </div>

            <div className="customization-section">
              <h3>Logo Upload</h3>
              <input
                type="file"
                accept=".jpg,.jpeg,.png,.pdf,.ai"
                onChange={(e) => {
                  if (e.target.files[0]) {
                    handleLogoUpload(e.target.files[0]);
                  }
                }}
              />
              <p className="file-info">Accepted formats: JPG, PNG, PDF, AI</p>
            </div>

            <div className="pricing-section">
              <h3>Pricing</h3>
              <div className="price">
                ${getPrice(selectedProduct).toFixed(2)}
                {user && user.account_type === 'wholesale' && user.wholesale_approved && (
                  <span className="wholesale-badge">Wholesale Price</span>
                )}
                {user && user.account_type === 'wholesale' && !user.wholesale_approved && (
                  <span className="pending-badge">Pending Wholesale Approval</span>
                )}
              </div>
            </div>

            <button 
              className="quote-button"
              onClick={handleRequestQuote}
              disabled={!customization.business_name}
            >
              Request Quote
            </button>
          </div>
        </div>
      </div>
    );
  };

  const ProductCatalog = () => {
    const categories = [...new Set(products.map(p => p.category))];

    return (
      <div className="catalog-container">
        <div className="catalog-header">
          <h2>Fireworks Business Advertising Products</h2>
          <p>Professional signs, banners, and flags for your fireworks business</p>
        </div>

        {categories.map(category => (
          <div key={category} className="category-section">
            <h3>{category}</h3>
            <div className="products-grid">
              {products.filter(p => p.category === category).map(product => (
                <div key={product.id} className="product-card">
                  <img src={product.image_url} alt={product.name} />
                  <div className="product-info">
                    <h4>{product.name}</h4>
                    <p>{product.description}</p>
                    <div className="price">
                      ${getPrice(product).toFixed(2)}
                      {user && user.account_type === 'wholesale' && user.wholesale_approved && (
                        <span className="wholesale-badge">Wholesale</span>
                      )}
                    </div>
                    <div className="sizes">
                      Sizes: {product.sizes.join(', ')}
                    </div>
                    {product.customizable ? (
                      <button
                        className="customize-button"
                        onClick={() => {
                          setSelectedProduct(product);
                          setCurrentView('customize');
                        }}
                      >
                        Customize Product
                      </button>
                    ) : (
                      <button className="quote-button">Request Quote</button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

        <div className="custom-quote-section">
          <h3>Need Something Custom?</h3>
          <p>Don't see what you're looking for? We can create custom advertising solutions for your fireworks business.</p>
          <button className="custom-quote-button">Request Custom Quote</button>
        </div>
      </div>
    );
  };

  const QuotesView = () => {
    useEffect(() => {
      fetchQuotes();
    }, []);

    return (
      <div className="quotes-container">
        <h2>Your Quote Requests</h2>
        {quotes.length === 0 ? (
          <p>No quote requests yet. Browse our products to get started!</p>
        ) : (
          <div className="quotes-list">
            {quotes.map(quote => (
              <div key={quote.id} className="quote-card">
                <h4>{quote.product_name}</h4>
                <p><strong>Business:</strong> {quote.business_name}</p>
                <p><strong>Quantity:</strong> {quote.quantity}</p>
                <p><strong>Status:</strong> <span className={`status ${quote.status}`}>{quote.status}</span></p>
                <p><strong>Requested:</strong> {new Date(quote.created_at).toLocaleDateString()}</p>
                {quote.message && <p><strong>Message:</strong> {quote.message}</p>}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const HomePage = () => (
    <div className="home-container">
      <div className="hero-section">
        <h1>Professional Advertising for Fireworks Businesses</h1>
        <p>Custom signs, banners, and flags designed specifically for fireworks retailers</p>
        <div className="cta-buttons">
          <button 
            className="cta-primary"
            onClick={() => setCurrentView('products')}
          >
            Browse Products
          </button>
          {!user && (
            <button 
              className="cta-secondary"
              onClick={() => setCurrentView('register')}
            >
              Create Account
            </button>
          )}
        </div>
      </div>

      <div className="features-section">
        <h2>Why Choose Our Advertising Solutions?</h2>
        <div className="features-grid">
          <div className="feature">
            <h3>🎆 Fireworks Specialized</h3>
            <p>Designed specifically for fireworks businesses with industry-appropriate messaging and compliance.</p>
          </div>
          <div className="feature">
            <h3>🎨 Custom Design</h3>
            <p>Upload your logo and customize text to create professional branded advertising materials.</p>
          </div>
          <div className="feature">
            <h3>💰 Wholesale Pricing</h3>
            <p>Special pricing for qualifying businesses. Apply for wholesale account for better rates.</p>
          </div>
          <div className="feature">
            <h3>🚀 Quick Turnaround</h3>
            <p>Fast production and shipping to get your advertising materials when you need them.</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>FireworksAds Pro</h1>
        </div>
        <div className="nav-links">
          <button 
            onClick={() => setCurrentView('home')}
            className={currentView === 'home' ? 'active' : ''}
          >
            Home
          </button>
          <button 
            onClick={() => setCurrentView('products')}
            className={currentView === 'products' ? 'active' : ''}
          >
            Products
          </button>
          {user && (
            <button 
              onClick={() => setCurrentView('quotes')}
              className={currentView === 'quotes' ? 'active' : ''}
            >
              My Quotes
            </button>
          )}
          {user ? (
            <div className="user-menu">
              <span>Welcome, {user.business_name}</span>
              {user.account_type === 'wholesale' && !user.wholesale_approved && (
                <span className="pending-approval">Wholesale Pending</span>
              )}
              {user.account_type === 'wholesale' && user.wholesale_approved && (
                <span className="wholesale-approved">Wholesale</span>
              )}
              <button onClick={handleLogout}>Logout</button>
            </div>
          ) : (
            <div className="auth-buttons">
              <button onClick={() => setCurrentView('login')}>Login</button>
              <button onClick={() => setCurrentView('register')}>Register</button>
            </div>
          )}
        </div>
      </nav>

      <main className="main-content">
        {currentView === 'home' && <HomePage />}
        {currentView === 'products' && <ProductCatalog />}
        {currentView === 'customize' && selectedProduct && <ProductCustomizer />}
        {currentView === 'login' && <LoginForm />}
        {currentView === 'register' && <RegisterForm />}
        {currentView === 'quotes' && user && <QuotesView />}
      </main>

      <footer className="footer">
        <p>&copy; 2025 FireworksAds Pro. Professional advertising solutions for fireworks businesses.</p>
      </footer>
    </div>
  );
}

export default App;