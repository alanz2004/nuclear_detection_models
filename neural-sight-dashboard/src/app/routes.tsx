
import { Routes, Route } from "react-router-dom";
import { ModelProvider } from "../context/ModelContext";

import MainLayout from "../components/layout/MainLayout";
import DashboardPage from "../features/dashboard/DashBoardPage";

const AppRoutes = () => {
  return (
    <ModelProvider>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="*" element={<div>Page Not Found</div>} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Route>
      </Routes>
    </ModelProvider>
  );
};

export default AppRoutes;