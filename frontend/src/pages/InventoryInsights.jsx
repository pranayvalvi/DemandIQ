
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
