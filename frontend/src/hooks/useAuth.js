/**
 * Custom hook for authentication.
 * Convenience wrapper around AuthContext.
 */
import { useAuth as useAuthContext } from '../contexts/AuthContext';

export const useAuth = () => {
  return useAuthContext();
};

export default useAuth;
