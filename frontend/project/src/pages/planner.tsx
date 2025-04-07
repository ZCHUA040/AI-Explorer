import { useState } from 'react';
import { format } from 'date-fns';
import { Calendar, Clock, DollarSign, Tag } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ACTIVITY_CATEGORIES } from '@/lib/utils';
import ReactDatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom

const BUDGET_CATEGORIES = [
  { id: 'free', label: 'Free', description: 'Free of cost' },
  { id: 'low', label: '$', description: 'Under $50' },
  { id: 'medium', label: '$$', description: '$50 - $100' },
  { id: 'high', label: '$$$', description: 'Above $100' },
];

interface PlannerFilters {
  userid: number;
  title: string;  
  date: string;
  activity_type: string | null;
  price_category: string | null;
  start_time: string;
  end_time: string;
  interests: string[] | null;
}

export function PlannerPage() {
  const navigate = useNavigate(); // Initialize useNavigate hook

  const [filters, setFilters] = useState<PlannerFilters>({
    userid: 1, // Assuming a placeholder user ID, modify as needed
    title: '',
    date: format(new Date(), 'yyyy-MM-dd'),
    activity_type: null,
    price_category: null,
    start_time: '08:00',
    end_time: '21:00',
    interests: null,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("submitting");
    if (!filters.title) {
      toast.error('Please provide a title for the itinerary');
      return;
    }
    if (!filters.date) {
      toast.error('Please select a date');
      return;
    }

    console.log("Generating");
    toast.success('Generating your perfect itinerary...');

    try {
      const token = localStorage.getItem('token');
      console.log("Using token for generation:", token);
      // Make the API call to generate the itinerary
      const response = await fetch('http://127.0.0.1:5000/generate_itinerary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(filters),
      });

      const data = await response.json();
      console.log("Response from backend:", data);

      if (response.ok) {
        // Redirect to the generated itinerary page using the itineraryId returned
        const itineraryId = data.Itineraryid; // Ensure API returns this field
        console.log("Received itinerary ID:", itineraryId);
        if (itineraryId) {
          console.log("Redirecting to itinerary page...");
          navigate(`/itinerary/${itineraryId}`); // Use navigate for redirection
        } else {
          toast.error('Itinerary ID not found');
        }
      } else {
        toast.error(data.message || 'Failed to generate itinerary');
      }
    } catch (error) {
      toast.error('An error occurred while generating the itinerary');
      console.error(error);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container mx-auto py-8"
    >
      <div className="max-w-4xl mx-auto">
        <motion.h1 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
        >
          Plan Your Perfect Day in Singapore
        </motion.h1>

        <form onSubmit={handleSubmit} className="space-y-8 bg-white rounded-xl shadow-lg p-8">
          <motion.div 
            className="space-y-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Tag className="h-5 w-5 text-blue-600" />
              Title
            </h2>
            <Input
              type="text"
              value={filters.title}
              onChange={(e) => setFilters(prev => ({ ...prev, title: e.target.value }))}
              placeholder="Enter a title for your itinerary"
              className="w-full rounded-md border border-gray-200 px-3 py-2"
            />
          </motion.div>

          {/* Date Selection */}
          <motion.div 
            className="space-y-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Calendar className="h-5 w-5 text-blue-600" />
              Select Date
            </h2>
            <ReactDatePicker
              selected={new Date(filters.date)}
              onChange={(date: Date) => setFilters(prev => ({ ...prev, date: format(date, 'yyyy-MM-dd') }))}
              dateFormat="MMMM d, yyyy"
              minDate={new Date()}
              className="w-full rounded-md border border-gray-200 px-3 py-2"
            />
          </motion.div>

          {/* Start Time and End Time */}
          <motion.div 
            className="space-y-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Clock className="h-5 w-5 text-blue-600" />
              Set Start & End Time
            </h2>
            <div className="flex gap-4 items-center">
              <Input
                type="time"
                value={filters.start_time}
                onChange={(e) => setFilters(prev => ({ ...prev, start_time: e.target.value }))}
                className="w-32"
              />
              <span>to</span>
              <Input
                type="time"
                value={filters.end_time}
                onChange={(e) => setFilters(prev => ({ ...prev, end_time: e.target.value }))}
                className="w-32"
              />
            </div>
          </motion.div>

          {/* Budget Selection */}
          <motion.div 
            className="space-y-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <DollarSign className="h-5 w-5 text-blue-600" />
              Budget Preference
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {BUDGET_CATEGORIES.map((budget) => (
                <motion.button
                  key={budget.id}
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setFilters(prev => ({ ...prev, price_category: budget.label }))}
                  className={`p-4 rounded-lg border transition-colors ${
                    filters.price_category === budget.label
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-xl font-bold">{budget.label}</div>
                  <div className="text-sm text-gray-600">{budget.description}</div>
                </motion.button>
              ))}
            </div>
          </motion.div>

          {/* Interests Selection */}
          <motion.div 
            className="space-y-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Tag className="h-5 w-5 text-blue-600" />
              Interests
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {ACTIVITY_CATEGORIES.map((category) => (
                <motion.button
                  key={category.id}
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    setFilters(prev => ({
                      ...prev,
                      interests: prev.interests && prev.interests.includes(category.name)
                        ? null
                        : [category.name],
                    }));
                  }}
                  className={`p-4 rounded-lg border transition-colors ${
                    filters.interests && filters.interests.includes(category.name)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl mb-2">{category.icon}</div>
                  <div className="font-semibold">{category.name}</div>
                </motion.button>
              ))}
            </div>
          </motion.div>

          {/* Submit Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg shadow-lg transform transition hover:scale-[1.02]"
              size="lg"
            >
              Generate Itinerary
            </Button>
          </motion.div>
        </form>
      </div>
    </motion.div>
  );
}
