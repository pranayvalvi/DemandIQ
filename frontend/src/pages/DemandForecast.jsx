
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
