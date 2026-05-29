import { ToastProvider } from "./components/UI/ToastContext";
import "./components/UI/ToastContext.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import SalesList from "./pages/Sales/SalesList";
import SalesForm from "./pages/Sales/SalesForm";
import CommissionsList from "./pages/Commissions/CommissionsList";
import DashboardLayout from "./pages/Dashboard/Dashboard";
import Login from "./pages/Login/Login";
import { BaseLayout } from "./components/layout/BaseLayout";
import { AuthProvider, useAuth } from "./contexts/AuthContext";

const queryClient = new QueryClient();

function AppContent() {
  const { isCheckingSession, isAuthenticated } = useAuth();

  if (isCheckingSession) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-sm font-semibold text-slate-500">Verificando sessao...</p>
      </main>
    );
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<BaseLayout />}>
          <Route path="/" element={<DashboardLayout />} />
          <Route path="/vendas" element={<SalesList />} />
          <Route path="/vendas/nova" element={<SalesForm />} />
          <Route path="/vendas/:id" element={<SalesForm />} />
          <Route path="/comissoes" element={<CommissionsList />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ToastProvider>
          <AppContent />
        </ToastProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
