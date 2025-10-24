import { useState, useEffect } from 'react';
import { Search, Plus, Edit2, Trash2 } from 'lucide-react';
import { UserRole } from '../types';
import { InventoryItem } from '../types';

interface InventoryProps {
  userRole: UserRole;
}

const Inventory = ({ userRole }: InventoryProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);
  const [formData, setFormData] = useState({
    productId: '',
    productName: '',
    currentStock: 0,
    lowStockThreshold: 0
  });

  const canEdit = userRole === 'admin' || userRole === 'warehouse_manager';

  useEffect(() => {
    const storedItems = localStorage.getItem('inventoryItems');
    if (storedItems) {
      setItems(JSON.parse(storedItems));
    } else {
      const sampleData: InventoryItem[] = [
        { id: '1', productId: 'PLY-001', productName: 'Marine Plywood 18mm', currentStock: 450, lowStockThreshold: 100 },
        { id: '2', productId: 'PLY-002', productName: 'Commercial Plywood 12mm', currentStock: 320, lowStockThreshold: 80 },
        { id: '3', productId: 'PLY-003', productName: 'Flexible Plywood 6mm', currentStock: 75, lowStockThreshold: 100 },
        { id: '4', productId: 'PLY-004', productName: 'BWP Grade 19mm', currentStock: 560, lowStockThreshold: 120 },
        { id: '5', productId: 'PLY-005', productName: 'Decorative Plywood 8mm', currentStock: 190, lowStockThreshold: 50 }
      ];
      setItems(sampleData);
      localStorage.setItem('inventoryItems', JSON.stringify(sampleData));
    }
  }, []);

  const filteredItems = items.filter(item =>
    item.productId.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.productName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAdd = () => {
    setEditingItem(null);
    setFormData({ productId: '', productName: '', currentStock: 0, lowStockThreshold: 0 });
    setShowModal(true);
  };

  const handleEdit = (item: InventoryItem) => {
    setEditingItem(item);
    setFormData({
      productId: item.productId,
      productName: item.productName,
      currentStock: item.currentStock,
      lowStockThreshold: item.lowStockThreshold
    });
    setShowModal(true);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (editingItem) {
      const updatedItems = items.map(item =>
        item.id === editingItem.id ? { ...item, ...formData } : item
      );
      setItems(updatedItems);
      localStorage.setItem('inventoryItems', JSON.stringify(updatedItems));
    } else {
      const newItem: InventoryItem = {
        id: Date.now().toString(),
        ...formData
      };
      const updatedItems = [...items, newItem];
      setItems(updatedItems);
      localStorage.setItem('inventoryItems', JSON.stringify(updatedItems));
    }

    setShowModal(false);
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this item?')) {
      const updatedItems = items.filter(item => item.id !== id);
      setItems(updatedItems);
      localStorage.setItem('inventoryItems', JSON.stringify(updatedItems));
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Inventory Management</h1>
        <p className="text-slate-600">
          {canEdit ? 'Manage your product inventory' : 'View product inventory'}
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-200">
          <div className="flex flex-col sm:flex-row gap-4 justify-between">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
              />
            </div>

            {canEdit && (
              <button
                onClick={handleAdd}
                className="flex items-center justify-center gap-2 px-6 py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors"
              >
                <Plus className="w-4 h-4" />
                Add New Item
              </button>
            )}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Product ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Product Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Current Stock
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Low Stock Threshold
                </th>
                {canEdit && (
                  <th className="px-6 py-3 text-right text-xs font-semibold text-slate-700 uppercase tracking-wider">
                    Actions
                  </th>
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredItems.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 text-sm font-medium text-slate-800">{item.productId}</td>
                  <td className="px-6 py-4 text-sm text-slate-800">{item.productName}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`font-medium ${
                      item.currentStock <= item.lowStockThreshold
                        ? 'text-red-600'
                        : 'text-slate-800'
                    }`}>
                      {item.currentStock}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600">{item.lowStockThreshold}</td>
                  {canEdit && (
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleEdit(item)}
                          className="text-blue-600 hover:text-blue-800 p-2 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Edit"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-600 hover:text-red-800 p-2 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
            <h2 className="text-xl font-bold text-slate-800 mb-4">
              {editingItem ? 'Edit Product' : 'Add New Product'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Product ID
                </label>
                <input
                  type="text"
                  value={formData.productId}
                  onChange={(e) => setFormData({ ...formData, productId: e.target.value })}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Product Name
                </label>
                <input
                  type="text"
                  value={formData.productName}
                  onChange={(e) => setFormData({ ...formData, productName: e.target.value })}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Current Stock
                </label>
                <input
                  type="number"
                  value={formData.currentStock}
                  onChange={(e) => setFormData({ ...formData, currentStock: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
                  required
                  min="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Low Stock Threshold
                </label>
                <input
                  type="number"
                  value={formData.lowStockThreshold}
                  onChange={(e) => setFormData({ ...formData, lowStockThreshold: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
                  required
                  min="0"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2 border border-slate-300 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors"
                >
                  {editingItem ? 'Update' : 'Add'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Inventory;
