import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Dashboard from './pages/Dashboard';
import DemandForecast from './pages/DemandForecast';
import InventoryInsights from './pages/InventoryInsights';
import WhatIfAnalysis from './pages/WhatIfAnalysis';
import ModelPerformance from './pages/ModelPerformance';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/forecast" element={<DemandForecast />} />
          <Route path="/inventory" element={<InventoryInsights />} />
          <Route path="/what-if" element={<WhatIfAnalysis />} />
          <Route path="/model-performance" element={<ModelPerformance />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
