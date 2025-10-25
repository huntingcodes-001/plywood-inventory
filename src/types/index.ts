export type UserRole = 'admin' | 'salesperson' | 'warehouse_manager';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phoneNumber: string;
  emergencyContact: string;
  role: UserRole;
  status: 'invited' | 'active';
  // ADDED: Token for authenticated requests
  token?: string; 
}
export interface InventoryItem {
  id: string;
  productId: string;
  productName: string;
  currentStock: number;
  lowStockThreshold: number;
}

export interface Order {
  id: string;
  orderId: string;
  customerName: string;
  status: 'pending' | 'in-progress' | 'fulfilled';
  date: string;
  items: OrderItem[];
}

export interface OrderItem {
  productId: string;
  productName: string;
  quantity: number;
}
