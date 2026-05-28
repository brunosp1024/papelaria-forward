import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";

import { useAuth } from "../../contexts/AuthContext";
import { Sidebar } from "./Sidebar/Sidebar";
import { NavbarTop } from "./Navbar/NavbarTop";

export function BaseLayout() {
  const { logout } = useAuth();
  const location = useLocation();
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  async function handleLogout() {
    await logout();
  }

  function handleToggleSidebar() {
    setIsSidebarCollapsed((currentValue) => !currentValue);
  }

  return (
    <div className="dashboard-shell">
      <Sidebar collapsed={isSidebarCollapsed} currentPath={location.pathname} onLogout={handleLogout} />

      <main className="dashboard-content">
        <NavbarTop
          collapsed={isSidebarCollapsed}
          onToggleSidebar={handleToggleSidebar}
          onLogout={handleLogout}
        />

        <div className="dashboard-body">
          <Outlet />
        </div>
      </main>
    </div>
  );
}