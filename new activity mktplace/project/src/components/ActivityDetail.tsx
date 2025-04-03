import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Clock, ArrowLeft, Tag } from 'lucide-react';


export default function ActivityDetail() {
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
    <div>
      <Link
        to="/"
        className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="h-5 w-5 mr-2" />
        Back to marketplace
      </Link>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="relative h-96 justify-center items-center">
        <iframe src={activity.Image} width="1200" height="400"></iframe>
        </div>

        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <h1 className="text-3xl font-bold text-gray-900">{activity.Name}</h1>
            <div className="text-right">
              <span className={`${activity.Price === "0.0" ? 'bg-green-500 text-white' : 'bg-gray-100 text-gray-900'} px-4 py-2 rounded-full text-lg font-medium`}>
                ${ activity.Price }
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-6 mb-6 text-gray-600">
            <div className="flex items-center">
              {activity.Location}
            </div>
            <div className="flex items-center">
              <Tag className="h-5 w-5 mr-2" />
              {activity.Type}
            </div>
          </div>

          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold mb-2">About this activity</h2>
            <p className="text-gray-600 leading-relaxed">{activity.Description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
