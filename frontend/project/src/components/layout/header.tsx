import { useAuthStore } from '@/store/auth';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { MapPin, Menu, User } from 'lucide-react';

export function Header() {
  const { isAuthenticated, logout } = useAuthStore();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-sm">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center space-x-2">
          <MapPin className="h-8 w-8 text-indigo-600" />
          <span className="text-xl font-bold text-gray-900">SingaXplore</span>
        </Link>

        <nav className="hidden md:flex items-center space-x-6">
          <Link to="/activitymarketplace" className="text-gray-600 hover:text-gray-900">
          Activity Marketplace
          </Link>
          <Link to="/itineraries" className="text-gray-600 hover:text-gray-900">
          My Itineraries
          </Link>
          <Link to="/planner" className="text-gray-600 hover:text-gray-900">
          Plan New Trip
          </Link>
          {isAuthenticated ? (
            <>
              <Link to="/profile">
                <Button variant="outline" size="sm">
                  <User className="mr-2 h-4 w-4" />
                  Profile
                </Button>
              </Link>
              <Button variant="secondary" size="sm" onClick={() => logout()}>
                Sign Out
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="outline" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link to="/register">
                <Button size="sm">Sign Up</Button>
              </Link>
            </>
          )}
        </nav>

        <button className="md:hidden">
          <Menu className="h-6 w-6" />
        </button>
      </div>
    </header>
  );
}