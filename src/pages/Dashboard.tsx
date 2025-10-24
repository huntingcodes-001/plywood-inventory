import { Package, ShoppingCart, Users, AlertTriangle } from 'lucide-react';
import { UserRole } from '../types';

interface DashboardProps {
  userRole: UserRole;
}

const Dashboard = ({ userRole }: DashboardProps) => {
  const getStats = () => {
    if (userRole === 'admin') {
      return [
        { label: 'Total Products', value: '156', icon: Package, color: 'bg-blue-500' },
        { label: 'Active Orders', value: '43', icon: ShoppingCart, color: 'bg-green-500' },
        { label: 'Total Users', value: '28', icon: Users, color: 'bg-purple-500' },
        { label: 'Low Stock Items', value: '12', icon: AlertTriangle, color: 'bg-red-500' }
      ];
    } else if (userRole === 'salesperson') {
      return [
        { label: 'My Orders', value: '18', icon: ShoppingCart, color: 'bg-green-500' },
        { label: 'Pending Orders', value: '7', icon: AlertTriangle, color: 'bg-amber-500' },
        { label: 'Products Available', value: '156', icon: Package, color: 'bg-blue-500' }
      ];
    } else {
      return [
        { label: 'Total Products', value: '156', icon: Package, color: 'bg-blue-500' },
        { label: 'Pending Fulfillment', value: '23', icon: ShoppingCart, color: 'bg-amber-500' },
        { label: 'Low Stock Items', value: '12', icon: AlertTriangle, color: 'bg-red-500' }
      ];
    }
  };

  const stats = getStats();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Dashboard</h1>
        <p className="text-slate-600">Welcome back! Here's an overview of your metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <p className="text-slate-600 text-sm font-medium mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-slate-800">{stat.value}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {[1, 2, 3, 4].map((item) => (
              <div key={item} className="flex items-center gap-4 pb-4 border-b border-slate-100 last:border-0">
                <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <Package className="w-5 h-5 text-slate-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-800">Order #{1000 + item} updated</p>
                  <p className="text-xs text-slate-500">{item} hour{item > 1 ? 's' : ''} ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            {userRole === 'admin' && (
              <>
                <button className="w-full text-left px-4 py-3 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                  <p className="font-medium text-slate-800">Add New Product</p>
                  <p className="text-xs text-slate-500">Create a new inventory item</p>
                </button>
                <button className="w-full text-left px-4 py-3 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                  <p className="font-medium text-slate-800">Invite User</p>
                  <p className="text-xs text-slate-500">Add a new team member</p>
                </button>
              </>
            )}
            {userRole === 'salesperson' && (
              <>
                <button className="w-full text-left px-4 py-3 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                  <p className="font-medium text-slate-800">Create New Order</p>
                  <p className="text-xs text-slate-500">Start a new customer order</p>
                </button>
                <button className="w-full text-left px-4 py-3 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                  <p className="font-medium text-slate-800">Check Order Status</p>
                  <p className="text-xs text-slate-500">Track existing orders</p>
                </button>
              </>
            )}
            {userRole === 'warehouse_manager' && (
              <>
                <button className="w-full text-left px-4 py-3 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                  <p className="font-medium text-slate-800">Update Stock</p>
                  <p className="text-xs text-slate-500">Modify inventory levels</p>
                </button>
                <button className="w-full text-left px-4 py-3 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                  <p className="font-medium text-slate-800">Fulfill Orders</p>
                  <p className="text-xs text-slate-500">Process pending orders</p>
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
