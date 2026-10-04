import os

files = {
    "src/App.jsx": """
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import DemandForecast from './pages/DemandForecast';
import ModelPerformance from './pages/ModelPerformance';
import InventoryInsights from './pages/InventoryInsights';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
          <main className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/forecast" element={<DemandForecast />} />
              <Route path="/performance" element={<ModelPerformance />} />
              <Route path="/inventory" element={<InventoryInsights />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
""",
    "src/components/Sidebar.jsx": """
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, BarChart3, PackageSearch } from 'lucide-react';

const Sidebar = () => {
  const links = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Demand Forecast', path: '/forecast', icon: <TrendingUp size={20} /> },
    { name: 'Model Performance', path: '/performance', icon: <BarChart3 size={20} /> },
    { name: 'Inventory Insights', path: '/inventory', icon: <PackageSearch size={20} /> },
  ];

  return (
    <div className="w-64 bg-white border-r h-full flex flex-col">
      <div className="p-6 border-b text-center">
        <h1 className="text-2xl font-bold text-blue-600">DemandIQ</h1>
        <p className="text-sm text-gray-500 mt-1">Inventory Intelligence</p>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.name}
            to={link.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'
              }`
            }
          >
            {link.icon}
            <span className="font-medium">{link.name}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
""",
    "src/pages/Dashboard.jsx": """
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

  const cards = [
    { title: "Total Sales", value: stats.total_sales.toLocaleString(), icon: <Activity className="text-blue-500" /> },
    { title: "Total Revenue", value: '$' + stats.total_revenue.toLocaleString(), icon: <DollarSign className="text-green-500" /> },
    { title: "Total Products", value: stats.total_products, icon: <Package className="text-purple-500" /> },
    { title: "Total Stores", value: stats.total_stores, icon: <Store className="text-orange-500" /> }
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 mb-1">{card.title}</p>
              <h3 className="text-2xl font-bold text-gray-800">{card.value}</h3>
            </div>
            <div className="p-3 bg-gray-50 rounded-full">
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
""",
    "src/pages/DemandForecast.jsx": """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp } from 'lucide-react';

const DemandForecast = () => {
  const [formData, setFormData] = useState({
    store: '', product: '', category: '', forecast_date: new Date().toISOString().split('T')[0],
    price: 5.0, promotion: 0, holiday: 0, inventory: 100,
    lag_1: 30, lag_7: 35, lag_14: 30, lag_28: 32,
    rolling_mean_7: 32.5, rolling_mean_14: 31.0, rolling_mean_28: 31.5
  });

  const [prediction, setPrediction] = useState(null);
  const [options, setOptions] = useState({ stores: [], products: [], categories: [] });

  useEffect(() => {
    // In a real app we'd fetch all three in parallel
    const fetchData = async () => {
      try {
        const [st, pr, cat] = await Promise.all([
          axios.get('http://localhost:8000/api/stores'),
          axios.get('http://localhost:8000/api/products'),
          axios.get('http://localhost:8000/api/categories')
        ]);
        setOptions({
          stores: st.data.stores,
          products: pr.data.products,
          categories: cat.data.categories
        });
        if(st.data.stores.length) setFormData(f => ({...f, store: st.data.stores[0]}));
        if(pr.data.products.length) setFormData(f => ({...f, product: pr.data.products[0]}));
        if(cat.data.categories.length) setFormData(f => ({...f, category: cat.data.categories[0]}));
      } catch(e) { console.error(e); }
    };
    fetchData();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/predict', formData);
      setPrediction(res.data);
    } catch(err) { console.error(err); }
  };

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Demand Forecast</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Store</label>
                <select name="store" value={formData.store} onChange={handleChange} className="w-full p-2 border rounded-md">
                  {options.stores.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Product</label>
                <select name="product" value={formData.product} onChange={handleChange} className="w-full p-2 border rounded-md">
                  {options.products.map(p => <option key={p} value={p}>{p}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <select name="category" value={formData.category} onChange={handleChange} className="w-full p-2 border rounded-md">
                  {options.categories.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Forecast Date</label>
                <input type="date" name="forecast_date" value={formData.forecast_date} onChange={handleChange} className="w-full p-2 border rounded-md" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Price</label>
                <input type="number" step="0.01" name="price" value={formData.price} onChange={handleChange} className="w-full p-2 border rounded-md" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Promotion (1/0)</label>
                <select name="promotion" value={formData.promotion} onChange={handleChange} className="w-full p-2 border rounded-md">
                  <option value={0}>No</option>
                  <option value={1}>Yes</option>
                </select>
              </div>
            </div>
            
            <div className="pt-4 border-t">
               <h4 className="text-sm font-semibold text-gray-500 mb-3">Historical Context (Auto-populated in production)</h4>
               <div className="grid grid-cols-4 gap-2">
                 {['lag_1', 'lag_7', 'lag_14', 'lag_28'].map(l => (
                   <div key={l}>
                     <label className="block text-xs text-gray-500">{l}</label>
                     <input type="number" name={l} value={formData[l]} onChange={handleChange} className="w-full p-1 text-sm border rounded" />
                   </div>
                 ))}
               </div>
            </div>

            <button type="submit" className="w-full bg-blue-600 text-white font-medium py-2 px-4 rounded-md hover:bg-blue-700 transition">
              Generate Forecast
            </button>
          </form>
        </div>

        <div>
          {prediction ? (
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 p-6 rounded-xl shadow-md text-white text-center">
              <TrendingUp size={48} className="mx-auto mb-4 opacity-80" />
              <h3 className="text-lg font-medium opacity-90 mb-1">Predicted Demand</h3>
              <p className="text-5xl font-bold mb-4">{prediction.predicted_demand}</p>
              <div className="text-sm opacity-80 bg-black/20 rounded-lg p-3">
                <p>Store: {prediction.store}</p>
                <p>Product: {prediction.product}</p>
                <p>Date: {prediction.forecast_date}</p>
              </div>
            </div>
          ) : (
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 text-center text-gray-500 h-full flex flex-col justify-center">
              <p>Fill out the form and submit to generate an ML-powered forecast.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DemandForecast;
""",
    "src/pages/ModelPerformance.jsx": """
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ModelPerformance = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/model-performance')
      .then(res => setData(res.data.performance))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Model Performance</h2>
      
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
        <h3 className="text-xl font-semibold mb-4 text-gray-700">Metrics Comparison (Lower is better for MAE/RMSE)</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="p-3 font-semibold text-gray-600">Model</th>
                <th className="p-3 font-semibold text-gray-600">MAE</th>
                <th className="p-3 font-semibold text-gray-600">RMSE</th>
                <th className="p-3 font-semibold text-gray-600">R² Score</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, i) => (
                <tr key={i} className="border-b hover:bg-gray-50">
                  <td className="p-3 font-medium">{row.Model}</td>
                  <td className="p-3">{row.MAE.toFixed(3)}</td>
                  <td className="p-3">{row.RMSE.toFixed(3)}</td>
                  <td className="p-3 text-blue-600 font-semibold">{row.R2.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80">
          <h4 className="font-semibold text-center mb-4">RMSE Comparison</h4>
          <ResponsiveContainer width="100%" height="80%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Model" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="RMSE" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80">
          <h4 className="font-semibold text-center mb-4">R² Comparison</h4>
          <ResponsiveContainer width="100%" height="80%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Model" />
              <YAxis domain={[0.8, 1]} />
              <Tooltip />
              <Bar dataKey="R2" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ModelPerformance;
""",
    "src/pages/InventoryInsights.jsx": """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PackageSearch, AlertTriangle, CheckCircle, ArrowUpCircle } from 'lucide-react';

const InventoryInsights = () => {
  const [formData, setFormData] = useState({
    store: 'Store_A', product: 'Apples', category: 'Produce', forecast_date: new Date().toISOString().split('T')[0],
    price: 5.0, promotion: 0, holiday: 0, inventory: 20,
    lag_1: 30, lag_7: 35, lag_14: 30, lag_28: 32,
    rolling_mean_7: 32.5, rolling_mean_14: 31.0, rolling_mean_28: 31.5
  });
  
  const [insight, setInsight] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/inventory-insights', formData);
      setInsight(res.data);
    } catch(err) { console.error(err); }
  };

  const getStatusIcon = (status) => {
    if (status === 'LOW STOCK') return <AlertTriangle className="text-red-500 w-12 h-12 mb-2" />;
    if (status === 'SUFFICIENT STOCK') return <CheckCircle className="text-green-500 w-12 h-12 mb-2" />;
    return <ArrowUpCircle className="text-blue-500 w-12 h-12 mb-2" />;
  };

  const getStatusColor = (status) => {
    if (status === 'LOW STOCK') return 'text-red-600 bg-red-50';
    if (status === 'SUFFICIENT STOCK') return 'text-green-600 bg-green-50';
    return 'text-blue-600 bg-blue-50';
  };

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Inventory Insights</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
           <h3 className="text-xl font-semibold mb-4 text-gray-700">Run Inventory Analysis</h3>
           <form onSubmit={handleSubmit} className="space-y-4">
             <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Current Inventory Stock</label>
                <input type="number" name="inventory" value={formData.inventory} 
                       onChange={(e) => setFormData({...formData, inventory: parseInt(e.target.value)})} 
                       className="w-full p-2 border rounded-md" />
              </div>
              <button type="submit" className="w-full bg-purple-600 text-white font-medium py-2 px-4 rounded-md hover:bg-purple-700 transition">
                Analyze Stock Levels
              </button>
           </form>
           <p className="text-sm text-gray-500 mt-4 text-center">Uses XGBoost prediction engine behind the scenes.</p>
        </div>

        {insight && (
          <div className="space-y-6">
            <div className={`p-8 rounded-xl shadow-sm border flex flex-col items-center justify-center text-center ${getStatusColor(insight.stock_status)}`}>
               {getStatusIcon(insight.stock_status)}
               <h3 className="text-3xl font-bold mb-2">{insight.stock_status}</h3>
               <p className="opacity-80">Based on predicted demand of {insight.predicted_demand} units.</p>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">Expected Shortage</p>
                <p className="text-2xl font-bold text-red-600">{insight.expected_shortage} units</p>
              </div>
              <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">Suggested Reorder</p>
                <p className="text-2xl font-bold text-blue-600">{insight.suggested_reorder} units</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InventoryInsights;
"""
}

import os

for path, content in files.items():
    full_path = os.path.join("frontend", path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

print("Generated frontend components and pages successfully.")
