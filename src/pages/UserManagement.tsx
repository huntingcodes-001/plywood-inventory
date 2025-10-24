import { useState, useEffect } from 'react';
import { Plus, Trash2, Check, X } from 'lucide-react';

interface WhitelistedUser {
  email: string;
  role: 'salesperson' | 'warehouse_manager';
  signedUp: boolean;
}

const UserManagement = () => {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<'salesperson' | 'warehouse_manager'>('salesperson');
  const [users, setUsers] = useState<WhitelistedUser[]>([]);

  useEffect(() => {
    const storedUsers = JSON.parse(localStorage.getItem('whitelistedUsers') || '[]');
    setUsers(storedUsers);
  }, []);

  const handleInvite = (e: React.FormEvent) => {
    e.preventDefault();

    if (users.some(u => u.email === email)) {
      alert('User already invited');
      return;
    }

    const newUser: WhitelistedUser = {
      email,
      role,
      signedUp: false
    };

    const updatedUsers = [...users, newUser];
    setUsers(updatedUsers);
    localStorage.setItem('whitelistedUsers', JSON.stringify(updatedUsers));

    setEmail('');
    setRole('salesperson');
  };

  const handleDelete = (userEmail: string) => {
    if (confirm('Are you sure you want to remove this user?')) {
      const updatedUsers = users.filter(u => u.email !== userEmail);
      setUsers(updatedUsers);
      localStorage.setItem('whitelistedUsers', JSON.stringify(updatedUsers));
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">User Management</h1>
        <p className="text-slate-600">Invite and manage users for your organization.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Invite New User</h2>

        <form onSubmit={handleInvite} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
                placeholder="user@example.com"
                required
              />
            </div>

            <div>
              <label htmlFor="role" className="block text-sm font-medium text-slate-700 mb-2">
                Role
              </label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value as 'salesperson' | 'warehouse_manager')}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
              >
                <option value="salesperson">Salesperson</option>
                <option value="warehouse_manager">Warehouse Manager</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="flex items-center gap-2 px-6 py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            Invite User
          </button>
        </form>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h2 className="text-lg font-bold text-slate-800">Current Users</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Role
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Signup Status
                </th>
                <th className="px-6 py-3 text-right text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {users.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                    No users invited yet
                  </td>
                </tr>
              ) : (
                users.map((user) => (
                  <tr key={user.email} className="hover:bg-slate-50">
                    <td className="px-6 py-4 text-sm text-slate-800">{user.email}</td>
                    <td className="px-6 py-4 text-sm text-slate-600 capitalize">
                      {user.role.replace('_', ' ')}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        user.signedUp
                          ? 'bg-green-100 text-green-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {user.signedUp ? 'Active' : 'Invited'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {user.signedUp ? (
                        <div className="flex items-center gap-2 text-green-600">
                          <Check className="w-5 h-5" />
                          <span className="text-sm font-medium">Signed Up</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-2 text-slate-400">
                          <X className="w-5 h-5" />
                          <span className="text-sm font-medium">Pending</span>
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => handleDelete(user.email)}
                        className="text-red-600 hover:text-red-800 p-2 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete user"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UserManagement;
