import React, { useState, useEffect } from 'react';
import { Search, Filter, X } from 'lucide-react';
import ActivityCard from './ActivityCard';

interface Activity {
  Activityid: string;
  Name: string;
  Type: string;
  Location: string;
  Price: number;
  PriceCategory: string;
}

interface Filters {
  priceRange: string;
  category: string;
}

export function ActivityMarketplace() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [showFilters, setShowFilters] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [filters, setFilters] = useState<Filters>({
    priceRange: 'all',
    category: 'all',
  });

  useEffect(() => {
    fetchActivities();
  }, []);

  const fetchActivities = async () => {
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('jwt');
      const response = await fetch('http://127.0.0.1:5000/get_all_activities', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch activities');
      }

      const data: Activity[] = await response.json();
      setActivities(data);
    } catch (error) {
      setError('Could not load activities. Please try again later.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchActivitiesByType = async (type: string) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('jwt');
      const response = await fetch('http://127.0.0.1:5000/get_activities_by_type', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Type: type }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch activities by type');
      }

      const data: Activity[] = await response.json();
      setActivities(data);
    } catch (error) {
      setError('Could not filter activities by type.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchActivitiesByPriceCategory = async (priceCategory: string) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('jwt');
      const response = await fetch('http://127.0.0.1:5000/get_activities_by_price_category', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "Price Category": priceCategory }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch activities by price category');
      }

      const data: Activity[] = await response.json();
      setActivities(data);
    } catch (error) {
      setError('Could not filter activities by price.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchActivitiesByTypeandPriceCategory = async (type: string, priceCategory: string) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('jwt');
      const response = await fetch('http://127.0.0.1:5000/get_activities_by_type_and_price_category', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "Price Category": priceCategory , "Type" : type}),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch activities by price category');
      }

      const data: Activity[] = await response.json();
      setActivities(data);
    } catch (error) {
      setError('Could not filter activities by type or price.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filterType: keyof Filters, value: string) => {
    const updatedFilters = { ...filters, [filterType]: value };
    setFilters(updatedFilters);
  
    if (updatedFilters.category !== 'all' && updatedFilters.priceRange !== 'all') {
      fetchActivitiesByTypeandPriceCategory(updatedFilters.category, updatedFilters.priceRange);
    } else if (updatedFilters.category !== 'all') {
      fetchActivitiesByType(updatedFilters.category);
    } else if (updatedFilters.priceRange !== 'all') {
      fetchActivitiesByPriceCategory(updatedFilters.priceRange);
    } else {
      fetchActivities();
    }
  };

  const resetFilters = () => {
    setFilters({ priceRange: 'all', category: 'all' });
    fetchActivities();
  };
  const parsedActivities = activities.map(activity => JSON.parse(activity));
  const filteredActivities = parsedActivities.filter(activity =>
    activity["Name"].toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Discover Singapore's Best Activities</h1>
      
      <div className="flex gap-4 mb-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            type="text"
            placeholder="Search activities..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <button 
          className={`flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 ${showFilters ? 'bg-gray-100' : ''}`}
          onClick={() => setShowFilters(!showFilters)}
        >
          <Filter className="h-5 w-5" />
          Filters
        </button>
      </div>

      {showFilters && (
        <div className="bg-white p-4 rounded-lg shadow-md mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="font-semibold text-gray-900">Filters</h2>
            <button
              onClick={resetFilters}
              className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1"
            >
              <X className="h-4 w-4" />
              Reset
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
              <select
                value={filters.priceRange}
                onChange={(e) => handleFilterChange('priceRange', e.target.value)}
                className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="all">All Prices</option>
                <option value="Free">Free</option>
                <option value="$">$</option>
                <option value="$$">$$</option>
                <option value="$$$">$$$</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                value={filters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="all">All Categories</option>
                <option value="Cultural & Heritage">Cultural & Heritage</option>
                <option value="Fitness & Wellness">Fitness & Wellness</option>
                <option value="Food & Beverage">Food & Beverage</option>
                <option value="Outdoor & Nature">Outdoor & Nature</option>
                <option value="Social & Community Events">Social & Community Events</option>
                <option value="Workshops & Classes">Workshops & Classes</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {loading ? (
        <p className="text-center text-gray-500">Loading activities...</p>
      ) : error ? (
        <p className="text-center text-red-500">{error}</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredActivities.length > 0 ? (
            filteredActivities.map((activity: Activity) => (
              <ActivityCard key={activity.Activityid} activity={activity} />
            ))
          ) : (
            <p className="text-center text-gray-500">No activities found.</p>
          )}
        </div>
      )}
    </div>
  );
}