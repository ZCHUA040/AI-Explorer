import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Clock, ArrowLeft, Tag, MapPin } from 'lucide-react';

export function ActivityDetail() {
  const { id } = useParams();
  const [activity, setActivity] = useState<any>(null); // Store activity details
  const [loading, setLoading] = useState<boolean>(true); // Track loading state
  const [error, setError] = useState<string>(''); // Handle errors if API call fails

  useEffect(() => {
    // Fetch activity by id from the API
    const fetchActivity = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/get_activity_by_id`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id }), // Send id as part of the request body
        });

        if (response.ok) {
          const data = await response.json();
          setActivity(data);
        } else {
          setError('Failed to fetch activity data');
        }
      } catch (err) {
        setError('An error occurred while fetching data');
      } finally {
        setLoading(false);
      }
    };

    fetchActivity();
  }, [id]); // Dependency on `id` to refetch when it changes

  if (loading) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Loading...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">{error}</h2>
        <Link to="/" className="text-indigo-600 hover:text-indigo-700 mt-4 inline-block">
          Return to marketplace
        </Link>
      </div>
    );
  }

  if (!activity) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Activity not found</h2>
        <Link to="/" className="text-indigo-600 hover:text-indigo-700 mt-4 inline-block">
          Return to marketplace
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <Link to="/activitymarketplace" className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-6">
          <ArrowLeft className="h-5 w-5 mr-2" />
          Back to marketplace
        </Link>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Map Section */}
          <div className="w-full h-[400px] bg-gray-200">
            <iframe 
              src={activity.Image}
              className="w-full h-full border-0"
              title="Location Map"
            />
          </div>

          {/* Content Section */}
          <div className="p-6">
            {/* Activity ID Badge */}
            <div className="mb-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                Activity ID: {activity.Activityid}
              </span>
            </div>

            {/* Header */}
            <div className="flex justify-between items-start mb-6">
              <h1 className="text-3xl font-bold text-gray-900">{activity.Name}</h1>
              <div className="flex flex-col items-end">
                <span className="text-2xl font-bold text-gray-900">${activity.Price}</span>
                <div className="flex items-center mt-2">
                  <span className="text-sm text-gray-500 mr-2">Price Category:</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    { activity["Price Category"] }
                  </span>
                </div>
              </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-4 mb-8">
              <div className="flex items-center text-gray-600">
                <Tag className="h-5 w-5 mr-2" />
                <span>{activity.Type}</span>
              </div>
              <div className="flex items-center text-gray-600">
                <MapPin className="h-5 w-5 mr-2" />
                <span>{activity.Location}</span>
              </div>
            </div>

            {/* Description */}
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold mb-4 text-gray-900">About this activity</h2>
              <div className="text-gray-600 space-y-4">
                <p>{activity.Description}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
