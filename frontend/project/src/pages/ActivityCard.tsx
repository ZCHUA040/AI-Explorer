import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Tag } from 'lucide-react';
import { Activity } from '../types/activity';
import culturalpic from "../images/winel-sutanto-kogTCZDMmgw-unsplash.jpg";
import fitnesspic from "../images/chuttersnap-EwEP4lQ82Co-unsplash.jpg";
import foodpic from "../images/davey-gravy-QnVBdXQabdw-unsplash.jpg";
import outdoorpic from "../images/alexandra-lowenthal-fiKq2Rnu0y0-unsplash.jpg";
import socialpic from "../images/satoshi-nitawaki-A24pQbk7wl8-unsplash.jpg";
import workshoppic from "../images/cx-insight-YloghyfD7e8-unsplash.jpg";

interface ActivityCardProps {
  activity: Activity;
}

export default function ActivityCard({ activity }: ActivityCardProps) {
  const categoryImages = {
    "Cultural & Heritage": culturalpic,
    "Fitness & Wellness": fitnesspic,
    "Food & Beverage": foodpic,
    "Outdoor & Nature": outdoorpic,
    "Social & Community Events": socialpic,
    "Workshops & Classes": workshoppic
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