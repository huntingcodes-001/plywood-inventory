import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Inventory from './pages/Inventory';
import UserManagement from './pages/UserManagement';
import OrderManagement from './pages/OrderManagement';
import OrderFulfillment from './pages/OrderFulfillment';
import OrderStatus from './pages/OrderStatus';
import StockAlerts from './pages/StockAlerts';
import Reports from './pages/Reports';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

function AppContent() {
  const [currentPage, setCurrentPage] = useState('login');
  const { currentUser, logout } = useAuth();

  useEffect(() => {
    if (currentUser) {
      setCurrentPage('dashboard');
    } else {
      setCurrentPage('login');
    }
  }, [currentUser]);

  useEffect(() => {
    const adminUser = {
      id: 'admin-1',
      email: 'admin@plywoodpro.com',
      firstName: 'Admin',
      lastName: 'User',
      phoneNumber: '+1234567890',
      emergencyContact: '+1234567891',
      role: 'admin' as const,
      status: 'active' as const
    };

    const users = JSON.parse(localStorage.getItem('users') || '[]');
    if (!users.find((u: any) => u.email === adminUser.email)) {
      users.push(adminUser);
      localStorage.setItem('users', JSON.stringify(users));
    }
  }, []);

  const handleLogout = () => {
    logout();
    setCurrentPage('login');
  };

  if (!currentUser) {
    if (currentPage === 'signup') {
      return <Signup onNavigate={setCurrentPage} />;
    }
    return <Login onNavigate={setCurrentPage} />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard userRole={currentUser.role} />;
      case 'inventory':
        return <Inventory userRole={currentUser.role} />;
      case 'user-management':
        return currentUser.role === 'admin' ? <UserManagement /> : <Dashboard userRole={currentUser.role} />;
      case 'order-management':
        return <OrderManagement />;
      case 'orders':
        return <OrderManagement />;
      case 'order-fulfillment':
        return <OrderFulfillment />;
      case 'order-status':
        return <OrderStatus />;
      case 'stock-alerts':
        return <StockAlerts />;
      case 'reports':
        return currentUser.role === 'admin' ? <Reports /> : <Dashboard userRole={currentUser.role} />;
      default:
        return <Dashboard userRole={currentUser.role} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar
        currentPage={currentPage}
        onNavigate={setCurrentPage}
        userRole={currentUser.role}
      />
      <div className="flex-1 flex flex-col">
        <Header
          userRole={currentUser.role}
          userName={`${currentUser.firstName} ${currentUser.lastName}`}
          onLogout={handleLogout}
        />
        <main className="flex-1 p-8">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
