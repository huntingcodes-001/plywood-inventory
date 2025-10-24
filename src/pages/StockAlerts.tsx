import { useEffect, useState } from 'react';
import { AlertTriangle } from 'lucide-react';
import { InventoryItem } from '../types';

const StockAlerts = () => {
  const [lowStockItems, setLowStockItems] = useState<InventoryItem[]>([]);

  useEffect(() => {
    const items = JSON.parse(localStorage.getItem('inventoryItems') || '[]');
    const alerts = items.filter((item: InventoryItem) =>
      item.currentStock <= item.lowStockThreshold
    );
    setLowStockItems(alerts);
  }, []);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Stock Alerts</h1>
        <p className="text-slate-600">Monitor products with low stock levels</p>
      </div>

      {lowStockItems.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertTriangle className="w-8 h-8 text-green-600" />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">All Stock Levels Good</h3>
          <p className="text-slate-600">No products are currently below their low stock threshold.</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-200 bg-red-50">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-red-600" />
              <h2 className="text-lg font-bold text-red-900">
                {lowStockItems.length} Product{lowStockItems.length !== 1 ? 's' : ''} Below Threshold
              </h2>
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
                    Threshold
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {lowStockItems.map((item) => {
                  const percentageRemaining = (item.currentStock / item.lowStockThreshold) * 100;
                  const isCritical = percentageRemaining < 50;

                  return (
                    <tr key={item.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4 text-sm font-medium text-slate-800">
                        {item.productId}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-800">
                        {item.productName}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="font-bold text-red-600">
                          {item.currentStock}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.lowStockThreshold}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          isCritical
                            ? 'bg-red-100 text-red-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}>
                          {isCritical ? 'Critical' : 'Low'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="px-6 py-4 bg-slate-50 border-t border-slate-200">
            <p className="text-sm text-slate-600">
              These products need restocking to maintain optimal inventory levels.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockAlerts;
