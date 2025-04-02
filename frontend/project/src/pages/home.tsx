import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { MapPin, Coffee, Compass, Bus, Camera } from 'lucide-react';
import { motion } from 'framer-motion';

export function HomePage() {
  return (
    <div className="relative">
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1525625293386-3f8f99389edd?q=80&w=2000&auto=format&fit=crop)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'brightness(0.5)',
        }}
      />
      
      <div className="relative z-10 min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center text-white px-4">
        <motion.h1 
          className="text-5xl md:text-7xl font-bold text-center mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Discover Your Perfect Day in Singapore
        </motion.h1>
        <motion.p 
          className="text-xl md:text-2xl text-center mb-12 max-w-2xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Explore the Lion City's hidden gems, from local hawker delights to stunning architectural marvels.
        </motion.p>
        
        <motion.div 
          className="flex flex-col sm:flex-row gap-4 mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <Link to="/register">
            <Button size="lg" className="min-w-[200px] bg-red-600 hover:bg-red-700">
              Start Exploring
            </Button>
          </Link>
          <Link to="/activities">
            <Button variant="outline" size="lg" className="min-w-[200px] bg-white/10 backdrop-blur-sm border-white/20">
              Browse Activities
            </Button>
          </Link>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 max-w-6xl w-full">
          <motion.div 
            className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <Coffee className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Local Flavors</h3>
            <p className="text-gray-200">Savor authentic Singaporean cuisine</p>
          </motion.div>
          <motion.div 
            className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
          >
            <Camera className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Photo Spots</h3>
            <p className="text-gray-200">Capture Instagram-worthy moments</p>
          </motion.div>
          <motion.div 
            className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <Bus className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Easy Transit</h3>
            <p className="text-gray-200">Navigate with smart transport tips</p>
          </motion.div>
          <motion.div 
            className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.9 }}
          >
            <Compass className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Local Guides</h3>
            <p className="text-gray-200">Follow curated local experiences</p>
          </motion.div>
        </div>
      </div>
    </div>
  );
}