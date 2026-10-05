import React from 'react';
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
