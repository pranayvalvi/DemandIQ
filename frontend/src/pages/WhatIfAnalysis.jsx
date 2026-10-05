import React, { useState, useEffect } from 'react';
import { getStores, getProducts, predictDemand } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

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
                          <Cell key={`cell-${index}`} fill={index === 0 ? '#94a3b8' : '#4f46e5'} />
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
