import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Clock,
  MapPin,
  UtensilsCrossed,
  Wallet as Walk,
  Calendar,
  Pencil,
  Share2,
  X,
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

export function SharedItineraryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  const [schedule, setSchedule] = useState<ScheduleItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);
  const [shareName, setShareName] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchItinerary = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/get_itinerary_by_itineraryid`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`, 
          },
          body: JSON.stringify({ Itineraryid: id }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch itinerary');
        }

        const data: Itinerary = await response.json();
        setItinerary(data);
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

  const formatTime = (timeRange: string) => {
    const [start, end] = timeRange.split('-');
    const formatTimeString = (time: string) => {
      const [hours, minutes] = time.split(':');
      const hour = parseInt(hours, 10);
      const period = hour >= 12 ? 'PM' : 'AM';
      const formattedHour = hour % 12 || 12;
      return `${formattedHour}:${minutes} ${period}`;
    };
    return (
      <div className="flex flex-col items-center bg-gray-50 rounded-lg px-3 py-2 shadow-sm">
        <span className="font-medium text-gray-800">{formatTimeString(start)}</span>
        <div className="w-12 border-t border-gray-200 my-1"></div>
        <span className="text-sm text-gray-500">{formatTimeString(end)}</span>
      </div>
    );
  };


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
            <h1 className="text-4xl font-bold text-gray-900">{itinerary?.Title}</h1>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-blue-600" />
                <div>
                  <div className="text-sm text-gray-500">Activity Date</div>
                  <div className="font-medium">{formatDate(itinerary?.Date ?? '')}</div>
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

          <div className="inline-flex gap-4 bg-white rounded-lg shadow-sm p-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span className="text-sm text-gray-600">Activities</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-amber-500"></div>
              <span className="text-sm text-gray-600">Travel</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
              <span className="text-sm text-gray-600">Meals</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="relative">
            <div className="absolute left-[120px] top-0 bottom-0 w-0.5 bg-gray-200"></div>

            <div className="space-y-8">
              {schedule.map((item, index) => {
                const content = (
                  <div
                    className={`rounded-lg p-4 ml-4 ${getColor(item)} transition hover:shadow-md ${
                      item.id ? 'cursor-pointer' : ''
                    }`}
                  >
                    <div className="absolute left-[-37px] top-1/2 transform -translate-y-1/2 w-4 h-4 bg-white rounded-full border-4 border-blue-500"></div>
                    <div className="flex items-start gap-3">
                      {getIcon(item)}
                      <div>
                        <h3 className="text-lg font-semibold mb-1">
                          {item.activity || item.travel || item.lunch}
                        </h3>
                      </div>
                    </div>
                  </div>
                );

                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex gap-6"
                  >
                    <div className="w-28">{formatTime(item.time)}</div>
                    <div className="flex-1 relative">
                      {item.id ? (
                        <Link to={`/activity/${item.id}`}>{content}</Link>
                      ) : (
                        content
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
