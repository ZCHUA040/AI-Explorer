import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { motion } from 'framer-motion';
import { Calendar, Share2, Plus } from 'lucide-react';

interface Itinerary {
  Itineraryid: number;
  Userid: number;
  Title: string;
  Date: string;
  Details: string;
  Created: string;
}

export function SharedItinerariesPage() {
  const [itineraries, setItineraries] = useState<Itinerary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    // Replace with your actual API endpoint
    const fetchItineraries = async () => {
      try {
        // Assuming you have an endpoint like '/api/get_my_itineraries'
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/get_shared_itineraries', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`, 
          },
          body: JSON.stringify({ Userid: 1 }), // Replace with actual user ID
        });

        if (!response.ok) {
          throw new Error('Failed to fetch itineraries');
        }

        const data: Itinerary[] = await response.json();
        setItineraries(data);
      } catch (err) {
        setError('Failed to fetch itineraries');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchItineraries();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }
  const parsedItineraries = itineraries.map(itinerary => JSON.parse(itinerary));
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container mx-auto py-8 px-4"
    >
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Shared Itineraries</h1>
          <div className="flex gap-3">
            <Link
              to="/itineraries"
              className="flex items-center gap-2 bg-white text-gray-700 px-4 py-2 rounded-lg border border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-colors"
            >
              <Share2 className="h-5 w-5" />
              <span>My Itineraries</span>
            </Link>
            <Link
              to="/planner"
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="h-5 w-5" />
              <span>Generate Itinerary</span>
            </Link>
          </div>
        </div>

        <div className="grid gap-6">
          {parsedItineraries.map((itinerary : Itinerary) => (
            <Link key={itinerary.Itineraryid} to={`/shared_itinerary/${itinerary.Itineraryid}`}>
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="bg-white rounded-xl shadow-lg p-6 transition-shadow hover:shadow-xl"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                      {itinerary.Title}
                    </h2>

                  </div>
                  <div className="flex items-center text-gray-500">
                    <span>{itinerary.Date}</span>
                  </div>
                </div>
              </motion.div>
            </Link>
          ))}
        </div>
      </div>
    </motion.div>
  );
}



