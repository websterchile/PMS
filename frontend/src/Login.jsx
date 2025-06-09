import React, { useState } from 'react';
import axios from 'axios';

function Login({ setToken }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState(''); // For signup
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (isLogin) {
        // Login logic
        const response = await axios.post('http://localhost:8000/api/token/', {
          username,
          password,
        });
        const token = response.data.access;
        localStorage.setItem('token', token);
        setToken(token);
      } else {
        // Signup logic
        const response = await axios.post('http://localhost:8000/api/register/', {
          username,
          password,
          email,
        });
        setError('Signup successful! Please log in.');
        setIsLogin(true); // Switch to login after successful signup
      }
    } catch (err) {
      setError(isLogin ? 'Invalid credentials' : 'Signup failed. Username may already exist.');
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="card w-full max-w-md">
        <h2 className="text-3xl font-bold text-primary mb-6 text-center">
          {isLogin ? 'Login' : 'Sign Up'}
        </h2>
        {error && <p className="text-danger mb-4 text-center">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter username"
              required
            />
          </div>
          {!isLogin && (
            <div className="mb-4">
              <label className="block text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter email"
                required
              />
            </div>
          )}
          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter password"
              required
            />
          </div>
          <button type="submit" className="btn-primary w-full mb-4">
            {isLogin ? 'Login' : 'Sign Up'}
          </button>
          <p className="text-center text-gray-600">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
              }}
              className="text-primary hover:underline"
            >
              {isLogin ? 'Sign Up' : 'Login'}
            </button>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Login;