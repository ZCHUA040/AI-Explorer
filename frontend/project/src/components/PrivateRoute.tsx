import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const [isValid, setIsValid] = useState<boolean | null>(null);

  useEffect(() => {
    const validateToken = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setIsValid(false);
        return;
      }

      try {
        const res = await axios.get('http://localhost:5000/validateuserlogin', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setIsValid(res.status === 200);
      } catch {
        setIsValid(false);
      }
    };

    validateToken();
  }, []);

  if (isValid === null) return <div>Loading...</div>; // Or a spinner

  return isValid ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;