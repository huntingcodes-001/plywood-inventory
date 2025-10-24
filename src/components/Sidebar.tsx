import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  Users,
  FileText,
  CheckSquare,
  AlertTriangle,
  Search
} from 'lucide-react';
import { UserRole } from '../types';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  userRole: UserRole;
}

const Sidebar = ({ currentPage, onNavigate, userRole }: SidebarProps) => {
  const adminLinks = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'inventory', label: 'Inventory', icon: Package },
    { id: 'orders', label: 'Orders', icon: ShoppingCart },
    { id: 'user-management', label: 'User Management', icon: Users },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'order-status', label: 'Order Status', icon: Search }
  ];

  const salespersonLinks = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'inventory', label: 'Inventory (View Only)', icon: Package },
    { id: 'order-management', label: 'Order Management', icon: ShoppingCart },
    { id: 'order-status', label: 'Order Status', icon: Search }
  ];

  const warehouseManagerLinks = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'inventory', label: 'Inventory (Full Access)', icon: Package },
    { id: 'order-fulfillment', label: 'Order Fulfillment', icon: CheckSquare },
    { id: 'stock-alerts', label: 'Stock Alerts', icon: AlertTriangle },
    { id: 'order-status', label: 'Order Status', icon: Search }
  ];

  const getLinks = () => {
    switch (userRole) {
      case 'admin':
        return adminLinks;
      case 'salesperson':
        return salespersonLinks;
      case 'warehouse_manager':
        return warehouseManagerLinks;
      default:
        return [];
    }
  };

  const links = getLinks();

  return (
    <div className="w-64 bg-slate-800 text-white min-h-screen">
      <div className="p-6">
        <div className="flex items-center gap-2 mb-8">
          <Package className="w-8 h-8 text-amber-500" />
          <h1 className="text-xl font-bold">PlywoodPro</h1>
        </div>

        <nav className="space-y-2">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = currentPage === link.id;

            return (
              <button
                key={link.id}
                onClick={() => onNavigate(link.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-amber-600 text-white'
                    : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="text-sm font-medium">{link.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
