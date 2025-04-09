import { useState } from 'react';
import { format } from 'date-fns';
import { Calendar, Clock, DollarSign, Tag } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Modal } from '../components/ui/modal';
import { ACTIVITY_CATEGORIES } from '../lib/utils';
import ReactDatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

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
}

export function PlannerPage() {
  const navigate = useNavigate();
  const [isErrorModalOpen, setIsErrorModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const [filters, setFilters] = useState<PlannerFilters>({
    userid: 1,
    title: '',
    date: format(new Date(), 'yyyy-MM-dd'),
    activity_type: null,
    price_category: null,
    start_time: '08:00',
    end_time: '21:00',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!filters.title) {
      toast.error('Please provide a title for the itinerary');
      return;
    }
    if (!filters.date) {
      toast.error('Please select a date');
      return;
    }

    toast.success('Generating your perfect itinerary...');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://127.0.0.1:5000/generate_itinerary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(filters),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.Error) {
          toast.error(data.Error);
          return;
        }
        const itineraryId = data.Itineraryid;
        if (itineraryId) {
          navigate(`/itinerary/${itineraryId}`);
        } else {
          toast.error('Itinerary ID not found');
        }
      } else {
        if (response.status === 500) {
          setErrorMessage('No activities found matching your criteria. Please try different options.');
          setIsErrorModalOpen(true);
        } else {
          toast.error(data.message || 'Failed to generate itinerary');
        }
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
      <Modal
        isOpen={isErrorModalOpen}
        onClose={() => setIsErrorModalOpen(false)}
        title="No Activities Found"
      >
        <p>{errorMessage}</p>
      </Modal>

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
              onChange={(date: Date | null) => {
                if (date) {
                  setFilters(prev => ({ ...prev, date: format(date, 'yyyy-MM-dd') }));
                }
              }}
              dateFormat="MMMM d, yyyy"
              minDate={new Date()}
              className="w-full rounded-md border border-gray-200 px-3 py-2"
            />
          </motion.div>

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
                  onClick={() => {
                    setFilters((prev) => ({
                      ...prev,
                      price_category: prev.price_category === budget.label ? "" : budget.label,
                    }));
                  }}
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

          <motion.div 
            className="space-y-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Tag className="h-5 w-5 text-blue-600" />
              Activity Type
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {ACTIVITY_CATEGORIES.map((category) => (
                <motion.button
                  key={category.id}
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    setFilters((prev) => ({
                      ...prev,
                      activity_type: prev.activity_type === category.name ? "" : category.name,
                    }));
                  }}
                  className={`p-4 rounded-lg border transition-colors ${
                    filters.activity_type === category.name
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