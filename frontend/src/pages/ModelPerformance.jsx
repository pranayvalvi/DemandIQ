import React, { useEffect, useState } from 'react';
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
