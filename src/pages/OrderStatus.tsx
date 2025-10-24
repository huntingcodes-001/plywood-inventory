import { useState } from 'react';
import { Search } from 'lucide-react';
import { Order } from '../types';

const OrderStatus = () => {
  const [orderId, setOrderId] = useState('');
  const [order, setOrder] = useState<Order | null>(null);
  const [notFound, setNotFound] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();

    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const foundOrder = orders.find((o: Order) => o.orderId === orderId);

    if (foundOrder) {
      setOrder(foundOrder);
      setNotFound(false);
    } else {
      setOrder(null);
      setNotFound(true);
    }
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

  const getStatusDescription = (status: string) => {
    switch (status) {
      case 'pending':
        return 'Your order has been received and is waiting to be processed.';
      case 'in-progress':
        return 'Your order is currently being prepared for delivery.';
      case 'fulfilled':
        return 'Your order has been completed and is ready for pickup or delivery.';
      default:
        return '';
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Order Status</h1>
        <p className="text-slate-600">Check the status of any order</p>
      </div>

      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
          <form onSubmit={handleSearch} className="mb-8">
            <label htmlFor="orderIdInput" className="block text-sm font-medium text-slate-700 mb-3">
              Enter Order ID
            </label>
            <div className="flex gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
                <input
                  id="orderIdInput"
                  type="text"
                  value={orderId}
                  onChange={(e) => setOrderId(e.target.value.toUpperCase())}
                  placeholder="e.g., ORD-1001"
                  className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
                  required
                />
              </div>
              <button
                type="submit"
                className="px-8 py-3 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors"
              >
                Search
              </button>
            </div>
          </form>

          {notFound && (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-slate-400" />
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-2">Order Not Found</h3>
              <p className="text-slate-600">
                No order found with ID: <span className="font-medium">{orderId}</span>
              </p>
            </div>
          )}

          {order && (
            <div className="border border-slate-200 rounded-xl overflow-hidden">
              <div className="bg-slate-50 px-6 py-4 border-b border-slate-200">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold text-slate-800">Order Details</h3>
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium capitalize ${getStatusColor(order.status)}`}>
                    {order.status.replace('-', ' ')}
                  </span>
                </div>
              </div>

              <div className="p-6 space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-slate-600 mb-1">Order ID</p>
                    <p className="font-semibold text-slate-800">{order.orderId}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-1">Customer</p>
                    <p className="font-semibold text-slate-800">{order.customerName}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-1">Date Placed</p>
                    <p className="font-semibold text-slate-800">{order.date}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-1">Status</p>
                    <p className="font-semibold text-slate-800 capitalize">{order.status.replace('-', ' ')}</p>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">{getStatusDescription(order.status)}</p>
                </div>

                <div>
                  <p className="text-sm font-medium text-slate-700 mb-3">Order Items</p>
                  <div className="border border-slate-200 rounded-lg overflow-hidden">
                    <table className="w-full">
                      <thead className="bg-slate-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700">Product</th>
                          <th className="px-4 py-3 text-right text-xs font-semibold text-slate-700">Quantity</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-200">
                        {order.items.map((item, idx) => (
                          <tr key={idx}>
                            <td className="px-4 py-3 text-sm text-slate-800">
                              <div>
                                <p className="font-medium">{item.productName}</p>
                                <p className="text-xs text-slate-500">{item.productId}</p>
                              </div>
                            </td>
                            <td className="px-4 py-3 text-sm text-slate-800 text-right font-medium">
                              {item.quantity}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${order.status === 'pending' ? 'bg-amber-500' : 'bg-green-500'}`}></div>
                      <span className="text-sm text-slate-600">Placed</span>
                    </div>
                    <div className="flex-1 h-0.5 bg-slate-200 mx-4"></div>
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${order.status === 'in-progress' ? 'bg-blue-500' : order.status === 'fulfilled' ? 'bg-green-500' : 'bg-slate-300'}`}></div>
                      <span className="text-sm text-slate-600">Processing</span>
                    </div>
                    <div className="flex-1 h-0.5 bg-slate-200 mx-4"></div>
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${order.status === 'fulfilled' ? 'bg-green-500' : 'bg-slate-300'}`}></div>
                      <span className="text-sm text-slate-600">Fulfilled</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OrderStatus;
