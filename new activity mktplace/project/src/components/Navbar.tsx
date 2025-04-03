import React from 'react';
import { Link } from 'react-router-dom';
import { Compass } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Compass className="h-8 w-8 text-indigo-600" />
            <span className="text-xl font-bold text-gray-900">SingaXplore</span>
          </Link>
          <div className="flex items-center space-x-4">
            <Link to="/" className="text-gray-600 hover:text-gray-900">Activities</Link>
            <Link to="/categories" className="text-gray-600 hover:text-gray-900">Categories</Link>
          </div>
        </div>
      </div>
    </nav>
  );
}