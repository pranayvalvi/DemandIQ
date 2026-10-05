import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {path}")

# Delete old pages to prevent routing confusion (we'll just overwrite them or make new ones)
base = "frontend/src"

api_js = """import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboardSummary = () => apiClient.get('/dashboard-summary').then(res => res.data);
export const getModelPerformance = () => apiClient.get('/model-performance').then(res => res.data.performance);
export const getSystemInfo = () => apiClient.get('/system-info').then(res => res.data);
export const getStores = () => apiClient.get('/stores').then(res => res.data.stores);
export const getProducts = () => apiClient.get('/products').then(res => res.data.products);
export const getCategories = () => apiClient.get('/categories').then(res => res.data.categories);
export const predictDemand = (payload) => apiClient.post('/predict', payload).then(res => res.data);
export const getInventoryInsights = (payload) => apiClient.post('/inventory-insights', payload).then(res => res.data);
"""
write_file(f"{base}/services/api.js", api_js)

sidebar_jsx = """import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, PackageSearch, SplitSquareHorizontal, LineChart, Settings, Activity } from 'lucide-react';

const Sidebar = () => {
  const menu = [
    { name: 'Dashboard', icon: <LayoutDashboard size={20} />, path: '/' },
    { name: 'Demand Forecast', icon: <TrendingUp size={20} />, path: '/forecast' },
    { name: 'Inventory Intelligence', icon: <PackageSearch size={20} />, path: '/inventory' },
    { name: 'What-If Analysis', icon: <SplitSquareHorizontal size={20} />, path: '/what-if' },
    { name: 'Model Performance', icon: <LineChart size={20} />, path: '/model-performance' },
    { name: 'Settings', icon: <Settings size={20} />, path: '/settings' },
  ];

  return (
    <div className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen border-r border-slate-800">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-white flex items-center tracking-tight">
          <Activity className="mr-2 text-indigo-500" />
          Demand<span className="text-indigo-500">IQ</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1 uppercase tracking-wider font-semibold">Retail Intelligence</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-1">
        {menu.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                isActive ? 'bg-indigo-600/10 text-indigo-400' : 'hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <span className="mr-3">{item.icon}</span>
            {item.name}
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center px-2 py-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 mr-2"></div>
          <span className="text-xs text-slate-400">API Connected</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
"""
write_file(f"{base}/components/layout/Sidebar.jsx", sidebar_jsx)

app_layout_jsx = """import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const AppLayout = () => {
  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 overflow-hidden font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-slate-200 h-16 flex items-center justify-between px-8 shrink-0">
          <div className="text-sm font-medium text-slate-500">
            Good morning, <span className="text-slate-900">Store Manager</span>
          </div>
          <div className="flex space-x-4">
            <select className="text-sm bg-slate-50 border border-slate-200 rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option>All Stores</option>
              <option>Store A</option>
            </select>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-8 bg-slate-50/50">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
"""
write_file(f"{base}/components/layout/AppLayout.jsx", app_layout_jsx)

app_jsx = """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Dashboard from './pages/Dashboard';
import DemandForecast from './pages/DemandForecast';
import InventoryInsights from './pages/InventoryInsights';
import WhatIfAnalysis from './pages/WhatIfAnalysis';
import ModelPerformance from './pages/ModelPerformance';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/forecast" element={<DemandForecast />} />
          <Route path="/inventory" element={<InventoryInsights />} />
          <Route path="/what-if" element={<WhatIfAnalysis />} />
          <Route path="/model-performance" element={<ModelPerformance />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
"""
write_file(f"{base}/App.jsx", app_jsx)


dashboard_jsx = """import React, { useEffect, useState } from 'react';
import { getDashboardSummary } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Package, TrendingUp, AlertTriangle, Crosshair } from 'lucide-react';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardSummary()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-8 bg-slate-200 w-64 rounded"></div>
        <div className="grid grid-cols-4 gap-6"><div className="h-32 bg-slate-200 rounded-xl"></div><div className="h-32 bg-slate-200 rounded-xl"></div><div className="h-32 bg-slate-200 rounded-xl"></div><div className="h-32 bg-slate-200 rounded-xl"></div></div>
      </div>
    );
  }

  if (!data) return <div className="text-center text-slate-500 py-12">Unable to load dashboard data.</div>;

  const { kpis, demand_trend, inventory_risk, category_demand, top_products } = data;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Retail Intelligence Overview</h2>
        <p className="text-slate-500 mt-1">Monitor demand, inventory risk, and recommended replenishment.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-100 transition-colors">
          <div className="flex justify-between items-start"><p className="text-sm font-medium text-slate-500">Forecasted Demand</p><TrendingUp size={16} className="text-indigo-500"/></div>
          <p className="text-3xl font-bold text-slate-900 mt-4">{kpis.avg_daily_demand.toLocaleString()} <span className="text-sm font-normal text-slate-500">units/day</span></p>
          <p className="text-xs text-emerald-600 mt-2 font-medium">↑ {kpis.demand_growth}% vs previous</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-100 transition-colors">
          <div className="flex justify-between items-start"><p className="text-sm font-medium text-slate-500">Low Stock Risk</p><AlertTriangle size={16} className="text-rose-500"/></div>
          <p className="text-3xl font-bold text-slate-900 mt-4">{kpis.low_stock_items} <span className="text-sm font-normal text-slate-500">items</span></p>
          <p className="text-xs text-rose-600 mt-2 font-medium">Requires attention</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-100 transition-colors">
          <div className="flex justify-between items-start"><p className="text-sm font-medium text-slate-500">Replenishment</p><Package size={16} className="text-emerald-500"/></div>
          <p className="text-3xl font-bold text-slate-900 mt-4">12 <span className="text-sm font-normal text-slate-500">orders</span></p>
          <p className="text-xs text-slate-500 mt-2 font-medium">Recommended for today</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-100 transition-colors">
          <div className="flex justify-between items-start"><p className="text-sm font-medium text-slate-500">Model Accuracy</p><Crosshair size={16} className="text-blue-500"/></div>
          <p className="text-3xl font-bold text-slate-900 mt-4">{kpis.model_r2.toFixed(3)} <span className="text-sm font-normal text-slate-500">R²</span></p>
          <p className="text-xs text-slate-500 mt-2 font-medium">Powered by XGBoost</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold text-slate-900">Demand Forecast Trend</h3>
          <span className="text-xs font-medium px-2 py-1 bg-slate-100 text-slate-600 rounded">7 Days</span>
        </div>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={demand_trend}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0"/>
              <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dy={10} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dx={-10} />
              <RechartsTooltip contentStyle={{borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
              <Line type="monotone" dataKey="actual" stroke="#94a3b8" strokeWidth={2} dot={{r: 4, strokeWidth: 2}} name="Actual" connectNulls />
              <Line type="monotone" dataKey="predicted" stroke="#4f46e5" strokeWidth={2} strokeDasharray="5 5" dot={{r: 4, strokeWidth: 2}} name="Forecast" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-6">Category Mix</h3>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={category_demand} layout="vertical" margin={{top: 0, right: 0, left: 0, bottom: 0}}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} width={80} tick={{fill: '#475569', fontSize: 13, fontWeight: 500}}/>
                <RechartsTooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}/>
                <Bar dataKey="value" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={24} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-6">Top Products by Forecasted Demand</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="text-slate-500 border-b border-slate-100">
                  <th className="pb-3 font-medium">Product</th>
                  <th className="pb-3 font-medium">Category</th>
                  <th className="pb-3 font-medium text-right">Forecast (Units)</th>
                  <th className="pb-3 font-medium text-right">Trend</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {top_products?.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    <td className="py-3 font-medium text-slate-900">{idx+1}. {item.product}</td>
                    <td className="py-3 text-slate-500">{item.category}</td>
                    <td className="py-3 text-right font-semibold text-indigo-600">{item.forecast.toFixed(1)}</td>
                    <td className="py-3 text-right">
                      {item.trend === 'up' ? <span className="text-emerald-500 inline-flex items-center"><TrendingUp size={14} className="mr-1"/></span> : <span className="text-rose-500 inline-flex items-center"><TrendingUp size={14} className="mr-1 rotate-180"/></span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
"""
write_file(f"{base}/pages/Dashboard.jsx", dashboard_jsx)

forecast_jsx = """import React, { useState, useEffect } from 'react';
import { getStores, getProducts, getCategories, predictDemand } from '../services/api';
import { Activity } from 'lucide-react';

const DemandForecast = () => {
  const [formData, setFormData] = useState({
    store: '', product: '', category: '', forecast_date: new Date().toISOString().split('T')[0],
    price: 5.0, promotion: 0, holiday: 0, inventory: 100,
    lag_1: 30, lag_7: 35, lag_14: 30, lag_28: 32,
    rolling_mean_7: 32.5, rolling_mean_14: 31.0, rolling_mean_28: 31.5
  });
  const [options, setOptions] = useState({ stores: [], products: [], categories: [] });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([getStores(), getProducts(), getCategories()]).then(([st, pr, cat]) => {
      setOptions({ stores: st, products: pr, categories: cat });
      if(st.length) setFormData(f => ({...f, store: st[0]}));
      if(pr.length) setFormData(f => ({...f, product: pr[0]}));
      if(cat.length) setFormData(f => ({...f, category: cat[0]}));
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await predictDemand(formData);
      setResult(res);
    } catch(err) { console.error(err); } finally { setLoading(false); }
  };

  const handleChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

  return (
    <div className="space-y-8 max-w-5xl">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Demand Forecast</h2>
        <p className="text-slate-500 mt-1">Generate ML-based demand forecasts for individual products.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">Store</label>
                <select name="store" value={formData.store} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-shadow">
                  {options.stores.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">Product</label>
                <select name="product" value={formData.product} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-shadow">
                  {options.products.map(p => <option key={p} value={p}>{p}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">Category</label>
                <select name="category" value={formData.category} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-shadow">
                  {options.categories.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">Forecast Date</label>
                <input type="date" name="forecast_date" value={formData.forecast_date} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-shadow" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">Price ($)</label>
                <input type="number" step="0.01" name="price" value={formData.price} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-shadow" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">Promotion Active</label>
                <select name="promotion" value={formData.promotion} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-shadow">
                  <option value={0}>No</option>
                  <option value={1}>Yes</option>
                </select>
              </div>
            </div>

            <div className="pt-6 border-t border-slate-100">
               <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">Historical Context</h4>
               <div className="grid grid-cols-4 gap-4">
                 {['lag_1', 'lag_7', 'lag_14', 'lag_28'].map(l => (
                   <div key={l}>
                     <label className="block text-xs text-slate-500 mb-1 font-medium">{l}</label>
                     <input type="number" name={l} value={formData[l]} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded p-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20 transition-shadow" />
                   </div>
                 ))}
               </div>
            </div>

            <button type="submit" disabled={loading} className="w-full bg-slate-900 hover:bg-slate-800 text-white font-medium py-3 rounded-lg transition-colors flex justify-center items-center">
              {loading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> : 'Generate Forecast'}
            </button>
          </form>
        </div>

        <div>
          {result ? (
            <div className="bg-indigo-600 rounded-xl shadow-lg border border-indigo-700 text-white overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="p-6 border-b border-indigo-500/50 flex justify-between items-center">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-100">Forecast Result</span>
                <Activity size={16} className="text-indigo-200"/>
              </div>
              <div className="p-8 text-center relative overflow-hidden">
                <div className="absolute -top-10 -right-10 w-32 h-32 bg-white rounded-full blur-3xl opacity-10"></div>
                <h3 className="text-xl font-medium text-indigo-100 mb-2">{result.product}</h3>
                <p className="text-sm text-indigo-200 mb-6">Predicted Demand</p>
                <div className="text-6xl font-bold tracking-tight text-white mb-2 relative z-10">
                  {result.predicted_demand.toFixed(1)}
                </div>
                <span className="text-sm text-indigo-200">units</span>
              </div>
              <div className="bg-indigo-900/50 p-6 space-y-3 text-sm">
                <div className="flex justify-between"><span className="text-indigo-200">Date</span><span className="font-medium text-white">{result.forecast_date}</span></div>
                <div className="flex justify-between"><span className="text-indigo-200">Store</span><span className="font-medium text-white">{result.store}</span></div>
                <div className="flex justify-between"><span className="text-indigo-200">Model Engine</span><span className="font-bold text-white">XGBoost</span></div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-slate-200 border-dashed h-full flex flex-col justify-center items-center p-8 text-center text-slate-500">
              <Activity size={32} className="mb-4 opacity-20"/>
              <p className="text-sm">Select parameters and generate a forecast to view results.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
export default DemandForecast;
"""
write_file(f"{base}/pages/DemandForecast.jsx", forecast_jsx)

whatif_jsx = """import React, { useState, useEffect } from 'react';
import { getStores, getProducts, predictDemand } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const WhatIfAnalysis = () => {
  const [formData, setFormData] = useState({
    store: '', product: '', category: 'Produce', forecast_date: new Date().toISOString().split('T')[0],
    price: 5.0, holiday: 0, inventory: 100,
    lag_1: 30, lag_7: 35, lag_14: 30, lag_28: 32,
    rolling_mean_7: 32.5, rolling_mean_14: 31.0, rolling_mean_28: 31.5
  });
  const [options, setOptions] = useState({ stores: [], products: [] });
  const [scenario, setScenario] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([getStores(), getProducts()]).then(([st, pr]) => {
      setOptions({ stores: st, products: pr });
      if(st.length) setFormData(f => ({...f, store: st[0]}));
      if(pr.length) setFormData(f => ({...f, product: pr[0]}));
    });
  }, []);

  const handleRunScenario = async () => {
    setLoading(true);
    try {
      const dataWithoutPromo = { ...formData, promotion: 0 };
      const dataWithPromo = { ...formData, promotion: 1 };
      
      const [resOff, resOn] = await Promise.all([
        predictDemand(dataWithoutPromo),
        predictDemand(dataWithPromo)
      ]);
      
      const dOff = resOff.predicted_demand;
      const dOn = resOn.predicted_demand;
      const upliftPct = dOff > 0 ? ((dOn - dOff) / dOff) * 100 : 0;
      
      setScenario({
        withoutPromo: dOff,
        withPromo: dOn,
        upliftPercentage: upliftPct.toFixed(1),
        product: formData.product,
        chartData: [
          { name: 'Current (No Promo)', Demand: parseFloat(dOff.toFixed(1)) },
          { name: 'What-If (Promo ON)', Demand: parseFloat(dOn.toFixed(1)) }
        ]
      });
    } catch (err) { console.error(err); } finally { setLoading(false); }
  };

  return (
    <div className="space-y-8 max-w-5xl">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">What-If Analysis</h2>
        <p className="text-slate-500 mt-1">Explore how pricing and promotions may affect expected demand.</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-6">Scenario Builder</h3>
        <div className="grid grid-cols-4 gap-6 mb-6">
          <div><label className="block text-xs font-medium text-slate-600 mb-2">Product</label><select name="product" value={formData.product} onChange={e => setFormData({...formData, product: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20">{options.products.map(p => <option key={p} value={p}>{p}</option>)}</select></div>
          <div><label className="block text-xs font-medium text-slate-600 mb-2">Store</label><select name="store" value={formData.store} onChange={e => setFormData({...formData, store: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20">{options.stores.map(s => <option key={s} value={s}>{s}</option>)}</select></div>
          <div><label className="block text-xs font-medium text-slate-600 mb-2">Base Price ($)</label><input type="number" step="0.01" value={formData.price} onChange={e => setFormData({...formData, price: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20" /></div>
          <div><label className="block text-xs font-medium text-slate-600 mb-2">Holiday Factor</label><select value={formData.holiday} onChange={e => setFormData({...formData, holiday: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20"><option value={0}>Normal Day</option><option value={1}>Holiday</option></select></div>
        </div>
        <div className="flex justify-end space-x-4">
          <button onClick={() => setScenario(null)} className="px-6 py-2 border border-slate-200 text-slate-600 font-medium rounded-lg hover:bg-slate-50 transition-colors">Reset</button>
          <button onClick={handleRunScenario} disabled={loading} className="px-6 py-2 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-lg transition-colors flex items-center">
            {loading ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div> : null}
            Run Scenario Comparison
          </button>
        </div>
      </div>

      {scenario && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="bg-slate-50 px-6 py-4 border-b border-slate-100 font-semibold text-slate-700">Current Scenario (No Promo)</div>
            <div className="p-8 text-center">
              <p className="text-4xl font-bold text-slate-800">{scenario.withoutPromo.toFixed(1)} <span className="text-lg font-normal text-slate-500">units</span></p>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-indigo-200 shadow-sm overflow-hidden shadow-indigo-100/50">
            <div className="bg-indigo-50 px-6 py-4 border-b border-indigo-100 font-semibold text-indigo-800 flex justify-between">
              What-If Scenario (Promo ON)
              <span className="text-xs font-bold bg-indigo-200 text-indigo-800 px-2 py-1 rounded">PROMOTION ACTIVE</span>
            </div>
            <div className="p-8 text-center relative">
              <p className="text-4xl font-bold text-indigo-600">{scenario.withPromo.toFixed(1)} <span className="text-lg font-normal text-indigo-400">units</span></p>
              <div className="absolute top-1/2 -left-6 transform -translate-y-1/2 bg-emerald-100 text-emerald-700 font-bold px-3 py-1 rounded-full text-sm shadow-sm border border-emerald-200 z-10">
                +{scenario.upliftPercentage}%
              </div>
            </div>
          </div>
          
          <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-6">
             <div className="md:col-span-1 bg-emerald-50 rounded-xl border border-emerald-100 p-6 flex flex-col justify-center text-center">
               <span className="text-xs font-bold uppercase tracking-widest text-emerald-600 mb-2">Business Recommendation</span>
               <p className="text-emerald-900 font-medium">Running a promotion is expected to increase demand for {scenario.product} by <strong className="text-emerald-700">{scenario.upliftPercentage}%</strong>.</p>
               <p className="text-emerald-800/80 text-sm mt-3 pt-3 border-t border-emerald-200/50">Consider increasing safety stock by at least {Math.ceil(scenario.withPromo - scenario.withoutPromo)} units before launching the promotion to prevent stockouts.</p>
             </div>
             
             <div className="md:col-span-2 bg-white rounded-xl border border-slate-200 p-6 h-64 shadow-sm">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={scenario.chartData} layout="vertical" margin={{top: 10, right: 30, left: 20, bottom: 5}}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9"/>
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} width={130} tick={{fill: '#475569', fontSize: 13, fontWeight: 500}}/>
                    <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}/>
                    <Bar dataKey="Demand" fill="#4f46e5" radius={[0, 4, 4, 0]} barSize={30}>
                      {
                        scenario.chartData.map((entry, index) => (
                          <cell key={`cell-${index}`} fill={index === 0 ? '#94a3b8' : '#4f46e5'} />
                        ))
                      }
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
             </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default WhatIfAnalysis;
"""
write_file(f"{base}/pages/WhatIfAnalysis.jsx", whatif_jsx)

inventory_jsx = """import React, { useState, useEffect } from 'react';
import { getStores, getProducts, getInventoryInsights } from '../services/api';
import { AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';

const InventoryInsights = () => {
  const [formData, setFormData] = useState({
    store: '', product: '', category: 'Produce', forecast_date: new Date().toISOString().split('T')[0],
    price: 5.0, promotion: 0, holiday: 0, inventory: 40,
    lag_1: 30, lag_7: 35, lag_14: 30, lag_28: 32,
    rolling_mean_7: 32.5, rolling_mean_14: 31.0, rolling_mean_28: 31.5
  });
  const [options, setOptions] = useState({ stores: [], products: [] });
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([getStores(), getProducts()]).then(([st, pr]) => {
      setOptions({ stores: st, products: pr });
      if(st.length) setFormData(f => ({...f, store: st[0]}));
      if(pr.length) setFormData(f => ({...f, product: pr[0]}));
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await getInventoryInsights(formData);
      setInsight(res);
    } catch(err) { console.error(err); } finally { setLoading(false); }
  };

  const getRiskColor = (status) => {
    if(status === 'LOW STOCK') return 'text-rose-600 bg-rose-50 border-rose-200';
    if(status === 'HIGH STOCK') return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-emerald-600 bg-emerald-50 border-emerald-200';
  };

  const calculateCoverage = (current, reorder) => {
    if(reorder <= 0) return 100;
    const pct = (current / reorder) * 100;
    return Math.min(100, pct);
  };

  return (
    <div className="space-y-8 max-w-5xl">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Inventory Intelligence</h2>
        <p className="text-slate-500 mt-1">Turn demand forecasts into replenishment decisions.</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <form onSubmit={handleSubmit} className="flex gap-4 items-end">
          <div className="flex-1"><label className="block text-xs font-semibold text-slate-600 mb-2">Store</label><select value={formData.store} onChange={e=>setFormData({...formData, store:e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20">{options.stores.map(s => <option key={s} value={s}>{s}</option>)}</select></div>
          <div className="flex-1"><label className="block text-xs font-semibold text-slate-600 mb-2">Product</label><select value={formData.product} onChange={e=>setFormData({...formData, product:e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20">{options.products.map(p => <option key={p} value={p}>{p}</option>)}</select></div>
          <div className="flex-1"><label className="block text-xs font-semibold text-slate-600 mb-2">Current Physical Stock</label><input type="number" value={formData.inventory} onChange={e=>setFormData({...formData, inventory:parseInt(e.target.value)})} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500/20" /></div>
          <button type="submit" className="bg-slate-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-slate-800 transition flex items-center">{loading ? 'Analyzing...' : 'Analyze Risk'}</button>
        </form>
      </div>

      {insight && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden animate-in fade-in duration-500">
          <div className={`px-6 py-4 border-b flex justify-between items-center ${getRiskColor(insight.stock_status)}`}>
            <span className="font-bold tracking-wider text-sm">{insight.product.toUpperCase()}</span>
            <div className="flex items-center font-bold text-sm">
              {insight.stock_status === 'LOW STOCK' ? <AlertTriangle size={16} className="mr-2"/> : <ShieldCheck size={16} className="mr-2"/>}
              {insight.stock_status === 'LOW STOCK' ? 'STOCKOUT RISK' : insight.stock_status}
            </div>
          </div>
          
          <div className="p-8 grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Current Stock</p>
              <p className="text-3xl font-bold text-slate-900">{insight.current_stock}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Forecasted Demand</p>
              <p className="text-3xl font-bold text-slate-900">{insight.predicted_demand}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Safety Stock (Z=1.65)</p>
              <p className="text-3xl font-bold text-slate-900">{insight.safety_stock}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Reorder Point</p>
              <p className="text-3xl font-bold text-indigo-600">{insight.target_inventory}</p>
            </div>
          </div>
          
          <div className="px-8 pb-8">
            
            <div className="mb-8">
               <div className="flex justify-between text-xs font-medium text-slate-500 mb-2">
                 <span>Current Coverage</span>
                 <span>Reorder Target ({insight.target_inventory})</span>
               </div>
               <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden flex">
                 <div className={`h-full ${insight.stock_status === 'LOW STOCK' ? 'bg-rose-500' : 'bg-emerald-500'}`} style={{width: `${calculateCoverage(insight.current_stock, insight.target_inventory)}%`}}></div>
               </div>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-6 flex flex-col md:flex-row justify-between items-center gap-4">
              <div>
                <h4 className="font-semibold text-slate-900">Recommended Order Quantity</h4>
                <p className="text-sm text-slate-500 mt-1">Mathematically calculated to prevent stockouts.</p>
              </div>
              <div className="flex items-center text-right shrink-0">
                <span className="text-4xl font-bold text-indigo-600">{insight.suggested_reorder}</span>
                <span className="text-indigo-600 font-medium ml-2">units</span>
              </div>
            </div>
            
            {insight.suggested_reorder > 0 && (
              <p className="text-sm text-rose-600 mt-4 flex items-center justify-center font-medium bg-rose-50 py-3 rounded-lg border border-rose-100">
                <AlertTriangle size={16} className="mr-2"/> Current stock is below the estimated reorder point. Immediate replenishment recommended.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
export default InventoryInsights;
"""
write_file(f"{base}/pages/InventoryInsights.jsx", inventory_jsx)

model_jsx = """import React, { useEffect, useState } from 'react';
import { getModelPerformance } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { CheckCircle2 } from 'lucide-react';

const ModelPerformance = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    getModelPerformance().then(setData).catch(console.error);
  }, []);

  if(!data.length) return <div className="p-10 text-center text-slate-500">Loading model metrics...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Model Performance</h2>
        <p className="text-slate-500 mt-1">Compare forecasting models and understand why XGBoost was selected.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-6">Model Leaderboard (Test Data)</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-100 text-slate-500">
                  <th className="pb-3 font-medium">Model</th>
                  <th className="pb-3 font-medium text-right">MAE</th>
                  <th className="pb-3 font-medium text-right">RMSE</th>
                  <th className="pb-3 font-medium text-right">R² Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {data.map((row, i) => (
                  <tr key={i} className={row.Model === 'XGBoost' ? 'bg-indigo-50/30' : 'hover:bg-slate-50/50 transition-colors'}>
                    <td className="py-4 font-medium text-slate-900">{row.Model}</td>
                    <td className="py-4 text-slate-600 text-right">{row.MAE.toFixed(3)}</td>
                    <td className="py-4 text-slate-600 text-right">{row.RMSE.toFixed(3)}</td>
                    <td className={`py-4 text-right font-semibold ${row.Model === 'XGBoost' ? 'text-indigo-600' : 'text-slate-700'}`}>
                      {row.R2.toFixed(3)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-lg text-white p-6 relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500 rounded-full blur-3xl opacity-20 -mr-10 -mt-10"></div>
          <div>
              <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 block">Selected Model</span>
              <h3 className="text-2xl font-bold text-white mb-6">XGBoost Regressor</h3>
              
              <div className="space-y-4 mb-8">
                <div className="flex items-start"><CheckCircle2 size={16} className="text-emerald-400 mr-3 mt-0.5 shrink-0"/> <span className="text-sm text-slate-300">Lowest Mean Absolute Error</span></div>
                <div className="flex items-start"><CheckCircle2 size={16} className="text-emerald-400 mr-3 mt-0.5 shrink-0"/> <span className="text-sm text-slate-300">Successfully captures non-linear promo effects</span></div>
                <div className="flex items-start"><CheckCircle2 size={16} className="text-emerald-400 mr-3 mt-0.5 shrink-0"/> <span className="text-sm text-slate-300">Robust to temporal outliers</span></div>
              </div>
          </div>
          
          <div className="pt-4 border-t border-slate-800">
            <span className="text-xs text-slate-500 uppercase tracking-wider block mb-2">Status</span>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Production Ready
            </span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-6 text-center">Root Mean Squared Error (Lower is Better)</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{top: 20, right: 30, left: 20, bottom: 5}}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9"/>
              <XAxis dataKey="Model" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 13}}/>
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 13}}/>
              <Tooltip cursor={{fill: '#f8fafc'}} formatter={v => v.toFixed(3)} contentStyle={{borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}/>
              <Bar dataKey="RMSE" fill="#6366f1" radius={[4, 4, 0, 0]} maxBarSize={60} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
export default ModelPerformance;
"""
write_file(f"{base}/pages/ModelPerformance.jsx", model_jsx)

settings_jsx = """import React, { useEffect, useState } from 'react';
import { getSystemInfo } from '../services/api';
import { Database, Server, Cpu } from 'lucide-react';

const Settings = () => {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    getSystemInfo().then(setInfo).catch(console.error);
  }, []);

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">System Settings</h2>
        <p className="text-slate-500 mt-1">Application configuration and system information.</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex items-center">
          <Server className="text-indigo-500 mr-3" size={20}/>
          <h3 className="font-semibold text-slate-900">API Connection</h3>
        </div>
        <div className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-900">Backend Status</p>
              <p className="text-sm text-slate-500 mt-1">http://localhost:8000/api</p>
            </div>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
              Connected
            </span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex items-center">
          <Cpu className="text-indigo-500 mr-3" size={20}/>
          <h3 className="font-semibold text-slate-900">Model Information</h3>
        </div>
        <div className="p-6">
          <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-6">
            <div>
              <dt className="text-sm font-medium text-slate-500">Active Engine</dt>
              <dd className="mt-1 text-sm text-slate-900 font-semibold">{info?.model || 'Loading...'}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">System Version</dt>
              <dd className="mt-1 text-sm text-slate-900">{info?.version || 'Loading...'}</dd>
            </div>
          </dl>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex items-center">
          <Database className="text-indigo-500 mr-3" size={20}/>
          <h3 className="font-semibold text-slate-900">Dataset Telemetry</h3>
        </div>
        <div className="p-6">
          <dl className="grid grid-cols-1 sm:grid-cols-3 gap-x-4 gap-y-6">
            <div>
              <dt className="text-sm font-medium text-slate-500">Historical Records</dt>
              <dd className="mt-1 text-xl text-slate-900 font-bold">{info ? info.dataset.records.toLocaleString() : '...'}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Tracked Products</dt>
              <dd className="mt-1 text-xl text-slate-900 font-bold">{info?.dataset.products || '...'}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Retail Stores</dt>
              <dd className="mt-1 text-xl text-slate-900 font-bold">{info?.dataset.stores || '...'}</dd>
            </div>
            <div className="sm:col-span-3 pt-4 border-t border-slate-100">
              <dt className="text-sm font-medium text-slate-500">Training Date Range</dt>
              <dd className="mt-1 text-sm text-slate-900 font-medium">
                {info ? `${info.dataset.start_date.split(' ')[0]} → ${info.dataset.end_date.split(' ')[0]}` : '...'}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
};
export default Settings;
"""
write_file(f"{base}/pages/Settings.jsx", settings_jsx)

print("All components written successfully.")
