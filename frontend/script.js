// Base URL for your Flask API (adjust if needed)
const apiBaseUrl = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
  // ----------------------------
  // Registration Form Handler
  // ----------------------------
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const email = document.getElementById('regEmail').value;
      const password = document.getElementById('regPassword').value;
      
      try {
        const response = await fetch(`${apiBaseUrl}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        const registerMessage = document.getElementById('registerMessage');
        registerMessage.textContent = data.message || data.error;
      } catch (error) {
        console.error('Registration error:', error);
        document.getElementById('registerMessage').textContent = 'Error registering user.';
      }
    });
  }

  // ----------------------------
  // Login Form Handler
  // ----------------------------
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const email = document.getElementById('loginEmail').value;
      const password = document.getElementById('loginPassword').value;
      
      try {
        const response = await fetch(`${apiBaseUrl}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        const loginMessage = document.getElementById('loginMessage');
        
        if (response.ok && data.token) {
          // Save the JWT token for future use
          localStorage.setItem('jwtToken', data.token);
          loginMessage.textContent = 'Login successful!';
        } else {
          loginMessage.textContent = data.error || 'Login failed.';
        }
      } catch (error) {
        console.error('Login error:', error);
        document.getElementById('loginMessage').textContent = 'Error logging in.';
      }
    });
  }

  // ----------------------------
  // Face Scan Form Handler
  // ----------------------------
  const scanForm = document.getElementById('scanForm');
  if (scanForm) {
    scanForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const fileInput = document.getElementById('scanImage');
      if (fileInput.files.length === 0) {
        document.getElementById('scanMessage').textContent = 'Please select an image file.';
        return;
      }
      
      const formData = new FormData();
      formData.append('image', fileInput.files[0]);
      
      try {
        const response = await fetch(`${apiBaseUrl}/scan`, {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        const scanMessage = document.getElementById('scanMessage');
        scanMessage.textContent = data.message || data.error;
      } catch (error) {
        console.error('Scan error:', error);
        document.getElementById('scanMessage').textContent = 'Error scanning face.';
      }
    });
  }
});
