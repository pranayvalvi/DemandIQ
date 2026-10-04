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
