import React, { useEffect, useState } from 'react';
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
