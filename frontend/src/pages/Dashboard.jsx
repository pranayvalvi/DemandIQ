import React, { useEffect, useState } from 'react';
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
