import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MapPin, LogOut, Lock, ImageIcon, List } from 'lucide-react';
import axios from 'axios';
import { useAuthStore } from '@/store/auth';
import toast from 'react-hot-toast';


export default function Navbar() {
  const { logout } = useAuthStore(); // no need to get `user` from here anymore
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [user, setUser] = useState<{ name: string; email: string, icon: string } | null>(null);

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
  
    if (!token) {
      console.warn('No token found, skipping logout API');
      logout();
      navigate('/login');
      return;
    }
  
    try {
      await axios.delete('http://localhost:5000/logout', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('Logout request sent');
    } catch (err: any) {
      console.error('Logout failed:', err);
      if (err.response) {
        console.error('Backend said:', err.response.data);
      }
      if (err.message) {
        console.error('Axios message:', err.message);
      }
    }
  
    // Always clear auth state and redirect
    logout();
    toast.success('Logout successful!');
    navigate('/');
  };


  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (!token) return;

      try {
        const res = await axios.get('http://localhost:5000/me', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(res.data);
      } catch (err) {
        console.error('Failed to fetch user profile:', err);
        logout();
        navigate('/login');
      }
    };

    fetchUser();
  }, []);

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/activitymarketplace" className="flex items-center space-x-2">
            <MapPin className="h-8 w-8 text-indigo-600" />
            <span className="text-xl font-bold text-gray-900">AiXplorer</span>
          </Link>

          {/* Nav Links */}
          <div className="flex items-center space-x-6 text-base text-gray-600">
            <Link to="/activitymarketplace" className="hover:text-gray-900">
              Activity Marketplace
            </Link>
            <Link to="/itineraries" className="hover:text-gray-900">
              My Itineraries
            </Link>
            <Link to="/planner" className="hover:text-gray-900">
              Plan New Trip
            </Link>

            {user && (
              <div className="relative">
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="font-medium text-indigo-600 hover:underline focus:outline-none"
                >
                  Hi, {user.name ?? 'User'}
                </button>

                {menuOpen && (
                  <div className="absolute right-0 mt-2 w-64 rounded-md bg-white shadow-lg border z-50">
                    {/* Greeting */}
                    <div className="p-4 border-b text-center">
                      <p className="text-sm text-gray-500 mb-1">Hi, welcome back! 😊</p>
                      <p className="font-semibold">{user.name}</p>
                      <p className="text-sm text-gray-500">{user.email}</p>
                    </div>

                    {/* Avatar */}
                    <div className="flex justify-center mt-4 mb-2">
                      <div className="h-14 w-14 rounded-full bg-indigo-100 flex items-center justify-center text-xl font-bold text-indigo-600">
                        {user.name?.charAt(0) ?? 'U'}
                      </div>
                    </div>

                    {/* Menu Options */}
                    <div className="p-2 space-y-1 text-sm">
                      <Link
                        to="/itineraries"
                        className="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 rounded-md"
                      >
                        <List className="h-4 w-4" />
                        My Itineraries
                      </Link>
                      <Link
                        to="/change-password"
                        className="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 rounded-md"
                      >
                        <Lock className="h-4 w-4" />
                        Change Password
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="flex items-center gap-2 text-red-500 w-full px-3 py-2 hover:bg-red-50 rounded-md"
                      >
                        <LogOut className="h-4 w-4" />
                        Log out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
