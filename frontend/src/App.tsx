import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { DashboardLayout } from "./components/layout/Dashboard";
import { Login } from "./components/auth/Login";
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

  return <DashboardLayout />;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
