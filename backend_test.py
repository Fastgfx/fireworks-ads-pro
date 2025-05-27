import requests
import sys
import uuid
import os
from datetime import datetime

class FireworksAPITester:
    def __init__(self, base_url="https://26d42d51-b47d-426a-97e7-2a5b46286634.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.user = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        self.test_password = "TestPass123!"
        self.test_business_name = "Test Fireworks Business"
        self.test_phone = "555-123-4567"
        self.uploaded_file_url = None
        self.customization_id = None
        self.quote_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    # Remove Content-Type for multipart/form-data
                    if 'Content-Type' in headers:
                        del headers['Content-Type']
                    response = requests.post(url, files=files, headers=headers)
                else:
                    response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Error details: {error_detail}")
                except:
                    print(f"Response text: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        print("\n=== Testing Health Check ===")
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        if success:
            print(f"Health check response: {response}")
        return success

    def test_register(self, account_type="regular"):
        """Test user registration"""
        print(f"\n=== Testing User Registration ({account_type}) ===")
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data={
                "email": self.test_user_email,
                "password": self.test_password,
                "business_name": self.test_business_name,
                "phone": self.test_phone,
                "account_type": account_type
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user = response['user']
            print(f"Registered user: {self.user}")
            return True
        return False

    def test_login(self):
        """Test user login"""
        print("\n=== Testing User Login ===")
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={
                "email": self.test_user_email,
                "password": self.test_password
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user = response['user']
            print(f"Logged in user: {self.user}")
            return True
        return False

    def test_get_current_user(self):
        """Test get current user endpoint"""
        print("\n=== Testing Get Current User ===")
        if not self.token:
            print("❌ No token available, skipping test")
            return False
            
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        if success:
            print(f"Current user: {response}")
        return success

    def test_get_products(self):
        """Test get products endpoint"""
        print("\n=== Testing Get Products ===")
        success, response = self.run_test(
            "Get Products",
            "GET",
            "products",
            200
        )
        if success and 'products' in response:
            print(f"Found {len(response['products'])} products")
            # Save first product ID for later tests
            if response['products']:
                self.product_id = response['products'][0]['id']
                print(f"Using product ID: {self.product_id}")
            return True
        return False

    def test_get_product_by_id(self):
        """Test get product by ID endpoint"""
        print("\n=== Testing Get Product by ID ===")
        if not hasattr(self, 'product_id'):
            print("❌ No product ID available, skipping test")
            return False
            
        success, response = self.run_test(
            "Get Product by ID",
            "GET",
            f"products/{self.product_id}",
            200
        )
        if success:
            print(f"Product details: {response['name']}")
        return success

    def test_file_upload(self):
        """Test file upload endpoint"""
        print("\n=== Testing File Upload ===")
        if not self.token:
            print("❌ No token available, skipping test")
            return False
            
        # Create a test image file
        test_file_path = "/tmp/test_logo.png"
        with open(test_file_path, "w") as f:
            f.write("Test file content")
            
        files = {'file': ('test_logo.png', open(test_file_path, 'rb'), 'image/png')}
        
        success, response = self.run_test(
            "File Upload",
            "POST",
            "upload",
            200,
            files=files
        )
        
        # Clean up test file
        os.remove(test_file_path)
        
        if success and 'file_url' in response:
            self.uploaded_file_url = response['file_url']
            print(f"Uploaded file URL: {self.uploaded_file_url}")
            return True
        return False

    def test_save_customization(self):
        """Test save customization endpoint"""
        print("\n=== Testing Save Customization ===")
        if not self.token or not hasattr(self, 'product_id'):
            print("❌ No token or product ID available, skipping test")
            return False
            
        success, response = self.run_test(
            "Save Customization",
            "POST",
            "customizations",
            200,
            data={
                "product_id": self.product_id,
                "business_name": self.test_business_name,
                "phone_number": self.test_phone,
                "logo_url": self.uploaded_file_url,
                "logo_position": {"x": 50, "y": 50}
            }
        )
        if success and 'id' in response:
            self.customization_id = response['id']
            print(f"Customization ID: {self.customization_id}")
            return True
        return False

    def test_get_customizations(self):
        """Test get customizations endpoint"""
        print("\n=== Testing Get Customizations ===")
        if not self.token:
            print("❌ No token available, skipping test")
            return False
            
        success, response = self.run_test(
            "Get Customizations",
            "GET",
            "customizations",
            200
        )
        if success and 'customizations' in response:
            print(f"Found {len(response['customizations'])} customizations")
            return True
        return False

    def test_request_quote(self):
        """Test request quote endpoint"""
        print("\n=== Testing Request Quote ===")
        if not self.token or not hasattr(self, 'product_id') or not self.user:
            print("❌ No token, product ID, or user available, skipping test")
            return False
            
        success, response = self.run_test(
            "Request Quote",
            "POST",
            "quotes",
            200,
            data={
                "user_email": self.user['email'],
                "business_name": self.test_business_name,
                "product_name": "Test Product",
                "customization_data": {
                    "business_name": self.test_business_name,
                    "phone_number": self.test_phone,
                    "logo_url": self.uploaded_file_url,
                    "logo_position": {"x": 50, "y": 50}
                },
                "quantity": 5,
                "message": "This is a test quote request"
            }
        )
        if success and 'id' in response:
            self.quote_id = response['id']
            print(f"Quote ID: {self.quote_id}")
            return True
        return False

    def test_get_quotes(self):
        """Test get quotes endpoint"""
        print("\n=== Testing Get Quotes ===")
        if not self.token:
            print("❌ No token available, skipping test")
            return False
            
        success, response = self.run_test(
            "Get Quotes",
            "GET",
            "quotes",
            200
        )
        if success and 'quotes' in response:
            print(f"Found {len(response['quotes'])} quotes")
            return True
        return False

    def run_all_tests(self):
        """Run all API tests"""
        tests = [
            self.test_health_check,
            self.test_register,
            self.test_login,
            self.test_get_current_user,
            self.test_get_products,
            self.test_get_product_by_id,
            self.test_file_upload,
            self.test_save_customization,
            self.test_get_customizations,
            self.test_request_quote,
            self.test_get_quotes
        ]
        
        for test in tests:
            test()
            
        # Print summary
        print(f"\n📊 Tests passed: {self.tests_passed}/{self.tests_run}")
        return self.tests_passed == self.tests_run

def main():
    # Setup
    tester = FireworksAPITester()
    
    # Run all tests
    success = tester.run_all_tests()
    
    # Return exit code
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
