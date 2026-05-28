import "./Sidebar.css";

type SidebarProps = {
  collapsed: boolean;
  onLogout?: () => Promise<void>;
};

export function Sidebar({ collapsed, onLogout }: SidebarProps) {
  async function handleLogout() {
    if (!onLogout) {
      return;
    }

    await onLogout();
  }

  return (
    <aside className={`sidebar ${collapsed ? "sidebar--collapsed" : ""}`}>

      <nav className="sidebar__nav" aria-label="Navegacao principal">
        <a className="sidebar__link" href="#dashboard-cards" title="Vendas">
          <span className="sidebar__link-content">
            <span className="sidebar__icon" aria-hidden="true">
              <svg className="sidebar__icon-svg" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" strokeWidth="1.8" />
                <path d="M7 9H17" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                <path d="M7 13H11" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
              </svg>
            </span>
            <span className="sidebar__label">Vendas</span>
          </span>
          <span className="sidebar__arrow" aria-hidden="true">
            <svg className="sidebar__arrow-svg" viewBox="0 0 20 20" fill="none">
              <path d="M7 4L13 10L7 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </span>
        </a>

        <a className="sidebar__link" href="#dashboard-summary" title="Comissoes">
          <span className="sidebar__link-content">
            <span className="sidebar__icon" aria-hidden="true">
              <svg className="sidebar__icon-svg" viewBox="0 0 24 24" fill="none">
                <path d="M5 19H19" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                <path d="M7 15L10 11L13 14L17 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="7" cy="15" r="1.2" fill="currentColor" />
                <circle cx="10" cy="11" r="1.2" fill="currentColor" />
                <circle cx="13" cy="14" r="1.2" fill="currentColor" />
                <circle cx="17" cy="9" r="1.2" fill="currentColor" />
              </svg>
            </span>
            <span className="sidebar__label">Comissoes</span>
          </span>
          <span className="sidebar__arrow" aria-hidden="true">
            <svg className="sidebar__arrow-svg" viewBox="0 0 20 20" fill="none">
              <path d="M7 4L13 10L7 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </span>
        </a>

        <button className="sidebar__link sidebar__link--button sidebar__link--logout" type="button" onClick={handleLogout} title="Sair">
          <span className="sidebar__link-content">
            <span className="sidebar__icon" aria-hidden="true">
              <svg className="sidebar__icon-svg" viewBox="0 0 24 24" fill="none">
                <path d="M9 4H6C4.9 4 4 4.9 4 6V18C4 19.1 4.9 20 6 20H9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                <path d="M16 17L20 13L16 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M20 13H10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
              </svg>
            </span>
            <span className="sidebar__label">Sair</span>
          </span>
        </button>
      </nav>
    </aside>
  );
}