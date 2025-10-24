import { useState, useEffect } from 'react';
import { CheckCircle } from 'lucide-react';
import { Order } from '../types';

const OrderFulfillment = () => {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    const storedOrders = localStorage.getItem('orders');
    if (storedOrders) {
      setOrders(JSON.parse(storedOrders));
    }
  }, []);

  const handleFulfill = (orderId: string) => {
    if (confirm('Mark this order as fulfilled?')) {
      const updatedOrders = orders.map(order =>
        order.id === orderId ? { ...order, status: 'fulfilled' as const } : order
      );
      setOrders(updatedOrders);
      localStorage.setItem('orders', JSON.stringify(updatedOrders));
    }
  };

  const pendingOrders = orders.filter(order => order.status === 'pending');

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Order Fulfillment</h1>
        <p className="text-slate-600">Process and fulfill pending orders</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h2 className="text-lg font-bold text-slate-800">Pending Orders</h2>
        </div>

        <div className="divide-y divide-slate-200">
          {pendingOrders.length === 0 ? (
            <div className="px-6 py-12 text-center text-slate-500">
              No pending orders to fulfill
            </div>
          ) : (
            pendingOrders.map((order) => (
              <div key={order.id} className="p-6 hover:bg-slate-50">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <h3 className="text-lg font-bold text-slate-800">{order.orderId}</h3>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                        Pending
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-slate-600 mb-1">Customer</p>
                        <p className="font-medium text-slate-800">{order.customerName}</p>
                      </div>
                      <div>
                        <p className="text-sm text-slate-600 mb-1">Date</p>
                        <p className="font-medium text-slate-800">{order.date}</p>
                      </div>
                    </div>

                    <div>
                      <p className="text-sm text-slate-600 mb-2">Items</p>
                      <div className="bg-slate-50 rounded-lg p-3">
                        {order.items.map((item, idx) => (
                          <div key={idx} className="flex justify-between py-1">
                            <span className="text-sm text-slate-700">{item.productName}</span>
                            <span className="text-sm font-medium text-slate-800">Qty: {item.quantity}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => handleFulfill(order.id)}
                    className="ml-6 flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors"
                  >
                    <CheckCircle className="w-5 h-5" />
                    Fulfill Order
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default OrderFulfillment;
