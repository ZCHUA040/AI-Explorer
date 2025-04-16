import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Clock,
  MapPin,
  UtensilsCrossed,
  Wallet as Walk,
  Calendar,
  Save,
  ArrowLeft,
  Edit,
} from 'lucide-react';

interface ScheduleItem {
  time: string;
  id?: number;
  activity?: string;
  travel?: string;
  lunch?: string;
}

interface Itinerary {
  Itineraryid: number;
  Userid: number;
  Title: string;
  Date: string;
  Details: string;
  Created: string;
}

export function EditItineraryPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  const [schedule, setSchedule] = useState<ScheduleItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [newActivityId, setNewActivityId] = useState<string>('');
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');

  useEffect(() => {
    const fetchItinerary = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/get_itinerary_by_itineraryid`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, 
          },
          body: JSON.stringify({ Itineraryid: id }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch itinerary');
        }

        const data: Itinerary = await response.json();
        setItinerary(data);
        setTitle(data.Title);
        setDate(data.Date.split('T')[0]); // Format date for input
        const parsed = JSON.parse(data.Details);
        setSchedule(parsed);
      } catch (err) {
        console.error('Failed to load itinerary:', err);
        setError('An error occurred while loading the itinerary.');
      } finally {
        setLoading(false);
      }
    };

    fetchItinerary();
  }, [id]);

  const handleSave = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://127.0.0.1:5000/update_itinerary`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          Itineraryid: id,
          Title: title,
          Date: date,
          Details: JSON.stringify(schedule),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update itinerary');
      }

      navigate(`/itinerary/${id}`);
    } catch (err) {
      console.error('Failed to update itinerary:', err);
      setError('An error occurred while updating the itinerary.');
    }
  };

  const handleUpdateActivityId = async (index: number) => {
    if (!newActivityId) {
      setError('Please enter a new activity ID');
      return;
    }
  
    try {
      const response = await fetch(`http://127.0.0.1:5000/get_activity_by_id`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: parseInt(newActivityId, 10) }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch activity');
      }
  
      const activityData = await response.json();
      const newActivityName = activityData.Name;
  
      const newSchedule = [...schedule];
  
      // Update current item with new activity
      newSchedule[index] = {
        ...newSchedule[index],
        id: parseInt(newActivityId, 10),
        activity: newActivityName,
      };
  
      // === UPDATE NEXT ITEM (if travel) ===
      if (index + 1 < newSchedule.length) {
        const nextItem = newSchedule[index + 1];
        if (nextItem.travel) {
          const match = nextItem.travel.match(/to (.+)$/i);
          const destination = match ? match[1] : 'destination';
          newSchedule[index + 1] = {
            ...nextItem,
            travel: `Travel from ${newActivityName} to ${destination}`,
          };
        }
      }
  
      // === UPDATE PREVIOUS ITEM (if travel) ===
      if (index - 1 >= 0) {
        const prevItem = newSchedule[index - 1];
        if (prevItem.travel) {
          const match = prevItem.travel.match(/from (.+?) to/i);
          const origin = match ? match[1] : 'origin';
          newSchedule[index - 1] = {
            ...prevItem,
            travel: `Travel from ${origin} to ${newActivityName}`,
          };
        }
      }
  
      setSchedule(newSchedule);
      setEditingIndex(null);
      setNewActivityId('');
    } catch (err) {
      console.error('Failed to update activity:', err);
      setError('Failed to update activity. Please check the activity ID.');
    }
  };
  
  const getIcon = (item: ScheduleItem) => {
    if (item.travel) return <MapPin className="h-5 w-5" />;
    if (item.lunch) return <UtensilsCrossed className="h-5 w-5" />;
    if (item.activity?.toLowerCase().includes('walk')) return <Walk className="h-5 w-5" />;
    return <Clock className="h-5 w-5" />;
  };

  const getColor = (item: ScheduleItem) => {
    if (item.travel) return 'bg-amber-100 text-amber-700';
    if (item.lunch) return 'bg-emerald-100 text-emerald-700';
    return 'bg-blue-100 text-blue-700';
  };

  const formatDate = (dateString: string) =>
    new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });

  if (loading) {
    return <div className="p-6 text-gray-500">Loading...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-500">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-12">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(`/itinerary/${id}`)}
                className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back</span>
              </button>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="text-4xl font-bold text-gray-900 bg-transparent border-b-2 border-transparent hover:border-gray-300 focus:border-blue-500 focus:outline-none transition-colors"
              />
            </div>
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Save className="h-4 w-4" />
              <span>Save Changes</span>
            </button>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-blue-600" />
                <div>
                  <div className="text-sm text-gray-500">Activity Date</div>
                  <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    className="font-medium bg-transparent border-b border-transparent hover:border-gray-300 focus:border-blue-500 focus:outline-none transition-colors"
                  />
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Clock className="h-5 w-5 text-blue-600" />
                <div>
                  <div className="text-sm text-gray-500">Created Date</div>
                  <div className="font-medium">{formatDate(itinerary?.Created ?? '')}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="space-y-8">
            {schedule.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="relative bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow"
              >
                <div className="grid grid-cols-1 gap-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      {getIcon(item)}
                      <div>
                        <div className="text-sm text-gray-500">Time</div>
                        <div className="font-medium">{item.time}</div>
                      </div>
                    </div>
                    {item.activity && (
                      <button
                        onClick={() => setEditingIndex(index)}
                        className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
                      >
                        <Edit className="h-4 w-4" />
                        <span>Change Activity</span>
                      </button>
                    )}
                  </div>

                  {item.id && (
                    <div className="flex items-center">
                      <span className="text-sm text-gray-500">Activity ID: {item.id}</span>
                    </div>
                  )}

                  {editingIndex === index && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                      <div className="flex gap-4">
                        <input
                          type="number"
                          value={newActivityId}
                          onChange={(e) => setNewActivityId(e.target.value)}
                          placeholder="Enter new activity ID"
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                          onClick={() => handleUpdateActivityId(index)}
                          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                          Update
                        </button>
                        <button
                          onClick={() => {
                            setEditingIndex(null);
                            setNewActivityId('');
                          }}
                          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}

                  <div className={`p-4 rounded-lg ${getColor(item)}`}>
                    {item.activity && <div className="font-medium">{item.activity}</div>}
                    {item.travel && <div className="font-medium">{item.travel}</div>}
                    {item.lunch && <div className="font-medium">{item.lunch}</div>}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
