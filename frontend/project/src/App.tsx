import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from '@/components/layout/header';
//import Navbar from './components/Navbar';
import PrivateHeader from '@/components/layout/privateheader'
import { HomePage } from '@/pages/home';
import { LoginPage } from '@/pages/SignIn';
import { RegisterPage } from './pages/SignUp';
import {ResetPasswordPage} from '@/pages/ResetPassword'
import {ForgotPasswordPage} from '@/pages/ForgotPassword'
import { PlannerPage } from './pages/planner';
import { ItinerariesPage } from './pages/ItinerariesPage';
import { ItineraryDetailPage } from './pages/ItineraryDetailPage';
import { SharedItinerariesPage } from './pages/SharedItinerariesPage';
import { SharedItineraryDetailPage } from './pages/SharedItineraryDetailPage';
import { ActivityMarketplace } from './pages/ActivityMarketplace';
import { ActivityDetail } from './pages/ActivityDetail';
import { EditItineraryPage } from './pages/EditItinerary';
import { ChangePasswordPage } from './pages/ChangePassword';
import PrivateRoute from './components/PrivateRoute';


function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <main>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<><Header /><LoginPage /></>} />
            <Route path="/register" element={<><Header /><RegisterPage /></>} />
            <Route path="/forgot-password" element={<><Header /><ForgotPasswordPage /></>} />
            <Route path="/reset-password" element={<><Header /><ResetPasswordPage /></>} />
            <Route path="/" element={<><Header /><HomePage /></>} />
            {/* Protected Routes (with PrivateHeader) */}
            <Route path="/itineraries" element={<PrivateRoute><><PrivateHeader /><ItinerariesPage /></></PrivateRoute>} />
            <Route path="/itinerary/:id" element={<PrivateRoute><><PrivateHeader /><ItineraryDetailPage /></></PrivateRoute>} />
            <Route path="/planner" element={<PrivateRoute><><PrivateHeader /><PlannerPage /></></PrivateRoute>} />
            <Route path="/shared_itineraries" element={<PrivateRoute><><PrivateHeader /><SharedItinerariesPage /></></PrivateRoute>} />
            <Route path="/shared_itinerary/:id" element={<PrivateRoute><><PrivateHeader /><SharedItineraryDetailPage /></></PrivateRoute>} />
            <Route path="/edit_itinerary/:id" element={<PrivateRoute><><PrivateHeader /><EditItineraryPage /></></PrivateRoute>} />
            <Route path="/activitymarketplace" element={<PrivateRoute><><PrivateHeader /><ActivityMarketplace /></></PrivateRoute>} />
            <Route path="/activity/:id" element={<PrivateRoute><><PrivateHeader /><ActivityDetail /></></PrivateRoute>} />
            <Route path="/change-password" element={<PrivateRoute><><PrivateHeader /><ChangePasswordPage /></></PrivateRoute>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;