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

export const SINGAPORE_REGIONS = [
  { id: 'central', name: 'Central', areas: ['Orchard', 'Marina Bay', 'Chinatown'] },
  { id: 'east', name: 'East', areas: ['Tampines', 'Changi', 'East Coast'] },
  { id: 'west', name: 'West', areas: ['Jurong', 'Clementi', 'Holland Village'] },
  { id: 'north', name: 'North', areas: ['Woodlands', 'Yishun', 'Thomson'] },
  { id: 'northeast', name: 'North-East', areas: ['Serangoon', 'Punggol', 'Sengkang'] },
] as const;

export const ACTIVITY_CATEGORIES = [
  { id: 'food', name: 'Food & Dining', icon: '🍜' },
  { id: 'culture', name: 'Culture & Heritage', icon: '🏮' },
  { id: 'nature', name: 'Nature & Parks', icon: '🌿' },
  { id: 'shopping', name: 'Shopping', icon: '🛍️' },
  { id: 'entertainment', name: 'Entertainment', icon: '🎭' },
] as const;