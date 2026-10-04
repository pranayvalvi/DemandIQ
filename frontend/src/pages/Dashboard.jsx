
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Package, Store, DollarSign, Activity } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/sales-summary')
      .then(res => setStats(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!stats) return <div className="text-center p-10">Loading...</div>;

  const formatRevenue = (value) => {
    if (value >= 1000000) return '$' + (value / 1000000).toFixed(1) + 'M';
    if (value >= 1000) return '$' + (value / 1000).toFixed(1) + 'K';
    return '$' + value.toLocaleString();
  };

  const cards = [
    { title: "Total Sales", value: stats.total_sales.toLocaleString(), icon: <Activity className="text-blue-500" /> },
    { title: "Total Revenue", value: formatRevenue(stats.total_revenue), icon: <DollarSign className="text-green-500" /> },
    { title: "Total Products", value: stats.total_products, icon: <Package className="text-purple-500" /> },
    { title: "Total Stores", value: stats.total_stores, icon: <Store className="text-orange-500" /> }
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between gap-2 overflow-hidden">
            <div className="min-w-0">
              <p className="text-sm text-gray-500 mb-1 truncate">{card.title}</p>
              <h3 className="text-2xl font-bold text-gray-800 truncate" title={card.value}>{card.value}</h3>
            </div>
            <div className="p-3 bg-gray-50 rounded-full shrink-0">
              {card.icon}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
         <h3 className="text-xl font-bold mb-4 text-gray-800">System Ready</h3>
         <p className="text-gray-600">The DemandIQ Machine Learning backend is connected and serving predictions using the tuned XGBoost model.</p>
      </div>
    </div>
  );
};

export default Dashboard;
