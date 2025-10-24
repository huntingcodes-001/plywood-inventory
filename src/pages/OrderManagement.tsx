import { useState, useEffect } from 'react';
import { Plus, Eye } from 'lucide-react';
import { Order } from '../types';

const OrderManagement = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  useEffect(() => {
    const storedOrders = localStorage.getItem('orders');
    if (storedOrders) {
      setOrders(JSON.parse(storedOrders));
    } else {
      const sampleOrders: Order[] = [
        {
          id: '1',
          orderId: 'ORD-1001',
          customerName: 'ABC Construction Ltd',
          status: 'pending',
          date: '2025-10-20',
          items: [
            { productId: 'PLY-001', productName: 'Marine Plywood 18mm', quantity: 50 }
          ]
        },
        {
          id: '2',
          orderId: 'ORD-1002',
          customerName: 'XYZ Furniture Co',
          status: 'in-progress',
          date: '2025-10-22',
          items: [
            { productId: 'PLY-002', productName: 'Commercial Plywood 12mm', quantity: 30 }
          ]
        }
      ];
      setOrders(sampleOrders);
      localStorage.setItem('orders', JSON.stringify(sampleOrders));
    }
  }, []);

  const handleViewDetails = (order: Order) => {
    setSelectedOrder(order);
    setShowModal(true);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-amber-100 text-amber-800';
      case 'in-progress':
        return 'bg-blue-100 text-blue-800';
      case 'fulfilled':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-slate-100 text-slate-800';
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Order Management</h1>
        <p className="text-slate-600">Create and manage customer orders</p>
      </div>

      <div className="mb-6">
        <button className="flex items-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors">
          <Plus className="w-5 h-5" />
          Create New Order
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h2 className="text-lg font-bold text-slate-800">Active Orders</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Order ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Customer Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-right text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {orders.filter(o => o.status !== 'fulfilled').map((order) => (
                <tr key={order.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 text-sm font-medium text-slate-800">{order.orderId}</td>
                  <td className="px-6 py-4 text-sm text-slate-800">{order.customerName}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getStatusColor(order.status)}`}>
                      {order.status.replace('-', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600">{order.date}</td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => handleViewDetails(order)}
                      className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium text-sm"
                    >
                      <Eye className="w-4 h-4" />
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && selectedOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6">
            <h2 className="text-xl font-bold text-slate-800 mb-4">Order Details</h2>

            <div className="space-y-4 mb-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Order ID</p>
                  <p className="font-semibold text-slate-800">{selectedOrder.orderId}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600 mb-1">Customer</p>
                  <p className="font-semibold text-slate-800">{selectedOrder.customerName}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600 mb-1">Status</p>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getStatusColor(selectedOrder.status)}`}>
                    {selectedOrder.status.replace('-', ' ')}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-slate-600 mb-1">Date</p>
                  <p className="font-semibold text-slate-800">{selectedOrder.date}</p>
                </div>
              </div>

              <div>
                <p className="text-sm text-slate-600 mb-2">Order Items</p>
                <div className="border border-slate-200 rounded-lg overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-slate-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-slate-700">Product ID</th>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-slate-700">Product Name</th>
                        <th className="px-4 py-2 text-right text-xs font-semibold text-slate-700">Quantity</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200">
                      {selectedOrder.items.map((item, idx) => (
                        <tr key={idx}>
                          <td className="px-4 py-2 text-sm text-slate-800">{item.productId}</td>
                          <td className="px-4 py-2 text-sm text-slate-800">{item.productName}</td>
                          <td className="px-4 py-2 text-sm text-slate-800 text-right">{item.quantity}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setShowModal(false)}
                className="px-6 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 font-medium rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderManagement;
