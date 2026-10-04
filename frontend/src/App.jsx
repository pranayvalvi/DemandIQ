
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import DemandForecast from './pages/DemandForecast';
import ModelPerformance from './pages/ModelPerformance';
import InventoryInsights from './pages/InventoryInsights';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
          <main className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/forecast" element={<DemandForecast />} />
              <Route path="/performance" element={<ModelPerformance />} />
              <Route path="/inventory" element={<InventoryInsights />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
