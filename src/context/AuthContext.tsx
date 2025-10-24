import { createContext, useContext, useState, ReactNode } from 'react';
import { User, UserRole } from '../types';

interface AuthContextType {
  currentUser: User | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (userData: Partial<User> & { password: string }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(() => {
    const stored = localStorage.getItem('currentUser');
    return stored ? JSON.parse(stored) : null;
  });

  const login = async (email: string, password: string) => {
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find((u: User) => u.email === email && u.status === 'active');

    if (!user) {
      throw new Error('Invalid credentials or account not activated');
    }

    setCurrentUser(user);
    localStorage.setItem('currentUser', JSON.stringify(user));
  };

  const signup = async (userData: Partial<User> & { password: string }) => {
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
  };

  return (
    <AuthContext.Provider value={{ currentUser, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
