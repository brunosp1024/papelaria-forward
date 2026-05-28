import { useState } from "react";

import {
  useCommissions,
  useCustomers,
  useProducts,
  useSales,
  useSellers,
} from "../../hooks";
import { useAuth } from "../../contexts/AuthContext";
import { NavbarTop } from "./NavbarTop";
import { Sidebar } from "./Sidebar";
import "./Dashboard.css";

function ResourceCard({
  title,
  count,
  isPending,
  isError,
}: {
  title: string;
  count?: number;
  isPending: boolean;
  isError: boolean;
}) {
  let value = count ?? 0;

  if (isPending) {
    value = 0;
  }

  return (
    <section className="resource-card">
      <h2 className="resource-card-title">{title}</h2>
      <p className="resource-card-value">{isPending ? "..." : value}</p>
      {isError ? <p className="resource-card-error">Erro ao carregar</p> : null}
    </section>
  );
}

export function DashboardLayout() {
  const { logout } = useAuth();
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const customers = useCustomers();
  const sellers = useSellers();
  const products = useProducts();
  const sales = useSales();
  const commissions = useCommissions();

  async function handleLogout() {
    await logout();
  }

  function handleToggleSidebar() {
    setIsSidebarCollapsed((currentValue) => !currentValue);
  }

  return (
    <div className="dashboard-shell">
      <Sidebar collapsed={isSidebarCollapsed} onLogout={handleLogout} />

      <main className="dashboard-content">
        <NavbarTop
          collapsed={isSidebarCollapsed}
          onToggleSidebar={handleToggleSidebar}
          onLogout={handleLogout}
        />

        <div className="dashboard-body">
          <header className="dashboard-header" id="dashboard-summary">
            <div>
              <h1 className="dashboard-title">Papelaria Forward</h1>
              <p className="dashboard-subtitle">Resumo de registros por recurso</p>
            </div>
          </header>

          <div className="dashboard-grid" id="dashboard-cards">
            <ResourceCard
              title="Clientes"
              count={customers.data?.count}
              isPending={customers.isPending}
              isError={customers.isError}
            />
            <ResourceCard
              title="Vendedores"
              count={sellers.data?.count}
              isPending={sellers.isPending}
              isError={sellers.isError}
            />
            <ResourceCard
              title="Produtos"
              count={products.data?.count}
              isPending={products.isPending}
              isError={products.isError}
            />
            <ResourceCard
              title="Vendas"
              count={sales.data?.count}
              isPending={sales.isPending}
              isError={sales.isError}
            />
            <ResourceCard
              title="Comissoes"
              count={commissions.data?.count}
              isPending={commissions.isPending}
              isError={commissions.isError}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
