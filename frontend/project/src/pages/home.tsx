import { MapPin, Coffee, Compass, Camera, Palette, Users} from 'lucide-react';



export function HomePage() {
  return (
    <div className="relative min-h-screen">
      {/* Hero Background Container */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        {/* Background Image with Object Fit */}
        <div 
          className="absolute inset-0 w-full h-full"
          style={{
            backgroundImage: 'url(https://images.unsplash.com/photo-1525625293386-3f8f99389edd?q=80&w=2000&auto=format&fit=crop)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            filter: 'brightness(0.5)',
            transform: 'scale(1.1)', // Slight scale to prevent white edges during animation
            animation: 'subtle-zoom 20s infinite alternate',
          }}
        />
        {/* Gradient Overlay */}
        <div 
          className="absolute inset-0 bg-gradient-to-b from-black/30 to-black/60"
          style={{ mixBlendMode: 'multiply' }}
        />
      </div>
      
      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center text-white px-4 py-20">
        <h1 className="text-5xl md:text-7xl font-bold text-center mb-6">
          Discover Singapore
        </h1>
        <p className="text-xl md:text-2xl text-center mb-12 max-w-2xl">
          Experience the vibrant culture, amazing cuisine, and stunning architecture of the Lion City
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 mb-16">
          <button className="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 rounded-lg text-lg font-semibold transition-colors">
            Start Exploring
          </button>
          <button className="px-8 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-lg font-semibold hover:bg-white/20 transition-colors">
            Learn More
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 max-w-6xl w-full">
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center">
            <Coffee className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Local Flavors</h3>
            <p className="text-gray-200">Savor authentic Singaporean cuisine</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center">
            <Camera className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Photo Spots</h3>
            <p className="text-gray-200">Capture Instagram-worthy moments</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center">
            <Palette className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Arts & Culture</h3>
            <p className="text-gray-200">Experience the Rich Heritage of Singapore</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg text-center">
            <Users className="h-10 w-10 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Meet Others</h3>
            <p className="text-gray-200">Share your joy with fellow explorers</p>
          </div>
        </div>
      </div>
    </div>
  );
}