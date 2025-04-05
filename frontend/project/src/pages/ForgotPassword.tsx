import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { KeyRound, Mail } from 'lucide-react';
import axios from 'axios';


export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    // Handle forgot password logic here
    try {
      await axios.post("http://localhost:5000/forgot-password", { email });
      setMessage("If an account exists, a reset link has been sent to your email.");
      setSubmitted(true);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to send reset email.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-100 mb-4">
            <KeyRound className="w-8 h-8 text-indigo-600" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900">Forgot password?</h2>
          <p className="text-gray-600 mt-2">
            Enter your email to reset your password
          </p>
        </div>

        {!submitted ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  placeholder="Enter your email"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-200 transition duration-200"
            >
              Send reset link
            </button>
            {message && <p className="text-green-600 text-sm text-center">{message}</p>}
            {error && <p className="text-red-500 text-sm text-center">{error}</p>}
          </form>
        ) : (
          <div className="text-center">
            <div className="mb-6 p-4 bg-green-50 rounded-lg">
              <p className="text-green-800">
                If an account exists with {email}, you will receive a password
                reset link shortly.
              </p>
            </div>
          </div>
        )}

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Remember your password?{' '}
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}