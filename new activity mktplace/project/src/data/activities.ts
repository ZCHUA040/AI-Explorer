import { Activity } from '../types/activity';

export const activities: Activity[] = [
  {
    id: '1',
    title: 'Gardens by the Bay Light Show',
    description: 'Experience the magical Garden Rhapsody light and sound show at Supertree Grove. Watch in wonder as the iconic Supertrees come alive with a dazzling display of lights choreographed to music.',
    image: 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?q=80&w=1920',
    priceRange: {
      min: 0,
      max: 0
    },
    region: 'central',
    category: 'entertainment',
    duration: '1 hour',
    rating: 4.8,
    reviews: 2453
  },
  {
    id: '2',
    title: 'Chinatown Food Tour',
    description: 'Embark on a culinary journey through Singapore\'s historic Chinatown. Sample local delicacies, learn about traditional cooking methods, and discover the rich cultural heritage of this vibrant district.',
    image: 'https://images.unsplash.com/photo-1569288063643-5d5369c4e04b?q=80&w=1920',
    priceRange: {
      min: 85,
      max: 120
    },
    region: 'central',
    category: 'food',
    duration: '3 hours',
    rating: 4.6,
    reviews: 1876
  },
  {
    id: '3',
    title: 'MacRitchie Nature Trail',
    description: 'Trek through Singapore\'s most popular nature trail. Experience the TreeTop Walk, spot local wildlife, and enjoy breathtaking views of the reservoir.',
    image: 'https://images.unsplash.com/photo-1542051841857-5f90071e7989?q=80&w=1920',
    priceRange: {
      min: 0,
      max: 0
    },
    region: 'north',
    category: 'nature',
    duration: '2-3 hours',
    rating: 4.7,
    reviews: 1543
  }
];