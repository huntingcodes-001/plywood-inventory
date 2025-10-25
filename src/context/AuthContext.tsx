import { createContext, useContext, useState, ReactNode } from 'react';
import { User, UserRole } from '../types';

interface AuthContextType {
  currentUser: User | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (userData: Partial<User> & { password: string }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define the FastAPI Backend URL
const BACKEND_URL = 'http://localhost:8000';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(() => {
    // Load currentUser and check for token on startup
    const stored = localStorage.getItem('currentUser');
    return stored ? JSON.parse(stored) : null;
  });

  const login = async (email: string, password: string) => {
    // --- INTEGRATION: Call FastAPI Login Endpoint ---
    const response = await fetch(`${BACKEND_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        // Handle custom FastAPI/HTTP errors
        const errorData = await response.json().catch(() => ({ detail: 'Login failed due to network or server error' }));
        // FastAPI uses the 'detail' field for errors
        throw new Error(errorData.detail || 'Invalid credentials');
    }

    const data = await response.json();
    
    // Structure the user object from the FastAPI response (data.user)
    const user: User = {
        id: data.user.id,
        email: data.user.email,
        // Use default empty string if data is null from API (e.g., first_name)
        firstName: data.user.first_name || '',
        lastName: data.user.last_name || '',
        phoneNumber: data.user.phone_number || '',
        emergencyContact: data.user.emergency_contact_number || '',
        role: data.user.role as UserRole, // Ensure role is correct type
        status: data.user.status,
        token: data.access_token, // Store the JWT token
    };

    setCurrentUser(user);
    
    // Store user data and token for session persistence
    localStorage.setItem('currentUser', JSON.stringify(user));
    localStorage.setItem('accessToken', data.access_token);
  };

  const signup = async (userData: Partial<User> & { password: string }) => {
    // NOTE: This logic remains mocked using localStorage,
    // only checking for whitelist status locally for now.
    const whitelistedUsers = JSON.parse(localStorage.getItem('whitelistedUsers') || '[]');
    const users = JSON.parse(localStorage.getItem('users') || '[]');

    const whitelisted = whitelistedUsers.find((u: any) => u.email === userData.email);

    if (!whitelisted) {
      throw new Error('Email not pre-registered. Contact administrator.');
    }

    const existingUser = users.find((u: User) => u.email === userData.email);
    if (existingUser && existingUser.status === 'active') {
      throw new Error('User already registered');
    }

    const newUser: User = {
      id: Date.now().toString(),
      email: userData.email!,
      firstName: userData.firstName!,
      lastName: userData.lastName!,
      phoneNumber: userData.phoneNumber!,
      emergencyContact: userData.emergencyContact!,
      role: whitelisted.role,
      status: 'active'
    };

    const updatedUsers = users.filter((u: User) => u.email !== userData.email);
    updatedUsers.push(newUser);
    localStorage.setItem('users', JSON.stringify(updatedUsers));

    const updatedWhitelist = whitelistedUsers.map((u: any) =>
      u.email === userData.email ? { ...u, signedUp: true } : u
    );
    localStorage.setItem('whitelistedUsers', JSON.stringify(updatedWhitelist));
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem('currentUser');
    localStorage.removeItem('accessToken'); // Clear the stored token
  };

  return (
    <AuthContext.Provider value={{ currentUser, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};