import React, { useState, useEffect } from 'react';
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
