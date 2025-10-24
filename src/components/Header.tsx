import { LogOut, User } from 'lucide-react';
import { UserRole } from '../types';

interface HeaderProps {
  userRole: UserRole;
  userName: string;
  onLogout: () => void;
}

const Header = ({ userRole, userName, onLogout }: HeaderProps) => {
  const getRoleDisplay = (role: UserRole) => {
    switch (role) {
      case 'admin':
        return 'Administrator';
      case 'salesperson':
        return 'Salesperson';
      case 'warehouse_manager':
        return 'Warehouse Manager';
      default:
        return role;
    }
  };

  return (
    <header className="bg-white border-b border-slate-200 px-8 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Inventory Management System</h2>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-slate-600" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-800">{userName}</p>
              <p className="text-xs text-slate-500">{getRoleDisplay(userRole)}</p>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
