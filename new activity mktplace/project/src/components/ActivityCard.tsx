import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Tag } from 'lucide-react';
import { Activity } from '../types/activity';

interface ActivityCardProps {
  activity: Activity;
}

export default function ActivityCard({ activity }: ActivityCardProps) {
  const categoryImages = {
    "Cultural & Heritage": "https://unsplash.com/photos/brown-and-black-floral-textile-kogTCZDMmgw",
    "Fitness & Wellness": "https://unsplash.com/photos/a-man-riding-a-bike-down-a-sidewalk-next-to-a-river-EwEP4lQ82Co",
    "Food & Beverage": "https://unsplash.com/photos/person-holding-stainless-steel-fork-and-knife-QnVBdXQabdw",
    "Outdoor & Nature": "https://unsplash.com/photos/a-wooden-walkway-in-the-middle-of-a-forest-5xD4tzm0MxM",
    "Social & Community Events": "https://unsplash.com/photos/a-crowd-of-people-standing-around-a-building-at-night-A24pQbk7wl8",
    "Workshops & Classes": "https://unsplash.com/photos/people-sitting-on-chair-in-front-of-table-YloghyfD7e8"
  };
  
  const activityImage = categoryImages[activity.Type as keyof typeof categoryImages]
  return (
    <Link to={`/activity/${activity.Activityid}`} className="group">
      <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 group-hover:scale-[1.02]">
        <div className="relative h-48">
          <img
            src={activityImage}
            alt={activity.Name}
            className="w-full h-full object-cover"
          />
        </div>
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{activity.Name}</h3>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <span className={`
              text-sm font-medium
              ${activity['Price Category'] == "0.0" 
                ? 'bg-green-500 text-white px-3 py-1 rounded-full' 
                : 'text-gray-600'}
            `}>
              {activity['Price Category']}
            </span>
            <div className="flex items-center">
              {activity.Location}
            </div>
            <div className="flex items-center">
              <Tag className="h-4 w-4 mr-1" />
              {activity.Type}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}