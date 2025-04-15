import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number) {
  return new Intl.NumberFormat('en-SG', {
    style: 'currency',
    currency: 'SGD',
  }).format(price);
}


export const ACTIVITY_CATEGORIES = [
  { id: 'fitness', name: 'Fitness & Wellness', icon: '⚽' },
  { id: 'culture', name: 'Cultural & Heritage', icon: '🏮' },
  { id: 'outdoor', name: 'Outdoor & Nature', icon: '🌿' },
  { id: 'workshops', name: 'Workshops & Classes', icon: '🎭' },
  { id: 'events', name: 'Social & Community Events', icon: '🎡' },
  { id: 'food', name: 'Food & Beverage', icon: '🍜' },
] as const;

export const ESTIMATED_DURATIONS = {
  food: 90, // 1.5 hours for dining
  culture: 120, // 2 hours for museums and heritage sites
  nature: 90, // 1.5 hours for parks and gardens
  shopping: 120, // 2 hours for shopping
  entertainment: 150, // 2.5 hours for entertainment venues
  attractions: 150, // 2.5 hours for tourist attractions
  sports: 120, // 2 hours for sports activities
} as const;