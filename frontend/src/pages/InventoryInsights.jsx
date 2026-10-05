import React, { useState, useEffect } from 'react';
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
