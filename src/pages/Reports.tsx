import { FileText, Download, TrendingUp, Package, ShoppingCart } from 'lucide-react';

const Reports = () => {
  const reportTypes = [
    {
      title: 'Inventory Summary',
      description: 'Complete overview of current stock levels',
      icon: Package,
      color: 'bg-blue-500'
    },
    {
      title: 'Sales Report',
      description: 'Order history and sales analytics',
      icon: TrendingUp,
      color: 'bg-green-500'
    },
    {
      title: 'Order Fulfillment',
      description: 'Order processing times and efficiency',
      icon: ShoppingCart,
      color: 'bg-purple-500'
    },
    {
      title: 'Low Stock Report',
      description: 'Products below threshold levels',
      icon: FileText,
      color: 'bg-red-500'
    }
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Reports</h1>
        <p className="text-slate-600">Generate and download business reports</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reportTypes.map((report, index) => {
          const Icon = report.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className={`${report.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>

              <h3 className="text-lg font-bold text-slate-800 mb-2">{report.title}</h3>
              <p className="text-sm text-slate-600 mb-4">{report.description}</p>

              <button className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium rounded-lg transition-colors">
                <Download className="w-4 h-4" />
                Generate Report
              </button>
            </div>
          );
        })}
      </div>

      <div className="mt-8 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Recent Reports</h2>
        <div className="space-y-3">
          {[1, 2, 3].map((item) => (
            <div key={item} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-slate-600" />
                <div>
                  <p className="font-medium text-slate-800">Inventory Summary Report</p>
                  <p className="text-xs text-slate-500">Generated on Oct {24 - item}, 2025</p>
                </div>
              </div>
              <button className="text-blue-600 hover:text-blue-800 font-medium text-sm">
                Download
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Reports;
