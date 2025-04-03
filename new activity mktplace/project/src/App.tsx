import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ActivityMarketplace from './components/ActivityMarketplace';
import ActivityDetail from './components/ActivityDetail';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<ActivityMarketplace />} />
            <Route path="/activity/:id" element={<ActivityDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;