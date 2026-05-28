import { Fragment, useState } from "react";
import { Link } from "react-router-dom";
import { useDeleteSale, useSales } from "../../hooks";
import { Sale } from "../../types";
import "./SalesList.css";
import { formatCurrency } from "../../utils/formatCurrency";
import { SaleItemsList } from "./components/SaleItemsList";
import ConfirmeDeleteModal from "../../components/UI/ConfirmDeleteModal";
import { useToast } from "../../components/UI/ToastContext";


function formatDateTime(value: string) {
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export default function SalesList() {
  const [expandedSaleIds, setExpandedSaleIds] = useState<Record<string, boolean>>({});
  const salesQuery = useSales({ page_size: "50", ordering: "-datetime" });
  const deleteSale = useDeleteSale();
  const [showModal, setShowModal] = useState(false);
  const [selectedSaleId, setSelectedSaleId] = useState<string | null>(null);
  const { showToast } = useToast();

  const sales: Sale[] = salesQuery.data?.results ?? [];

  function handleToggleRow(saleId: string) {
    setExpandedSaleIds((current) => ({
      ...current,
      [saleId]: !current[saleId],
    }));
  }


  async function handleModalDelete() {
    if (selectedSaleId) {
      try {
        await deleteSale.mutateAsync(selectedSaleId);
        showToast('Venda excluída com sucesso!', 'success');
      } catch (e) {
        showToast('Erro ao excluir venda.', 'error');
      }
    }
    handleClose();
  }

  async function handleDelete(saleId: string) {
    setSelectedSaleId(saleId);
    setShowModal(true);
  }

  const handleClose = () => {
    setShowModal(false);
    setSelectedSaleId(null);
  };

  return (
    <>
      <ConfirmeDeleteModal
        show={showModal}
        handleClose={handleClose}
        onConfirm={handleModalDelete}
      />
    
      <section className="sales-list">
        <header className="sales-list__header">
          <div>
            <h1 className="sales-list__title">Vendas realizadas</h1>
            <p className="sales-list__subtitle">Historico das vendas cadastradas</p>
          </div>
          <Link className="sales-list__add-button" to="/vendas/nova">
            Nova venda
          </Link>
        </header>

        <div className="sales-list__table-wrapper">
          <table className="sales-list__table">
            <thead>
              <tr>
                <th>Nota Fiscal</th>
                <th>Cliente</th>
                <th>Vendedor</th>
                <th>Data da Venda</th>
                <th>Valor Total</th>
                <th>Acoes</th>
              </tr>
            </thead>
            <tbody>
              {salesQuery.isPending ? (
                <tr>
                  <td className="sales-list__empty" colSpan={6}>
                    Carregando vendas...
                  </td>
                </tr>
              ) : null}

              {salesQuery.isError ? (
                <tr>
                  <td className="sales-list__empty sales-list__empty--error" colSpan={6}>
                    Erro ao carregar vendas.
                  </td>
                </tr>
              ) : null}

              {!salesQuery.isPending && !salesQuery.isError && sales.length === 0 ? (
                <tr>
                  <td className="sales-list__empty" colSpan={6}>
                    Lista vazia
                  </td>
                </tr>
              ) : null}

              {!salesQuery.isPending && !salesQuery.isError
                ? sales.map((sale) => {
                    const isExpanded = Boolean(expandedSaleIds[sale.id]);

                    return (
                      <Fragment key={sale.id}>
                        <tr>
                          <td>{sale.invoice_number}</td>
                          <td>{sale.customer.name}</td>
                          <td>{sale.seller.name}</td>
                          <td>{formatDateTime(sale.datetime)}</td>
                          <td>{formatCurrency(sale.total_value)}</td>
                          <td>
                            <div className="sales-list__actions">
                              <button
                                className="sales-list__link-button"
                                type="button"
                                onClick={() => handleToggleRow(sale.id)}
                              >
                                {isExpanded ? "Fechar" : "Ver mais"}
                              </button>
                              <Link className="sales-list__icon-button" to={`/vendas/${sale.id}`} aria-label="Editar venda">
                                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                  <path d="M4 20H8L18 10L14 6L4 16V20Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                                  <path d="M12.5 7.5L16.5 11.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                                </svg>
                              </Link>
                              <button
                                className="sales-list__icon-button sales-list__icon-button--danger"
                                type="button"
                                aria-label="Excluir venda"
                                onClick={() => handleDelete(sale.id)}
                                disabled={deleteSale.isPending}
                              >
                                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                  <path d="M4 7H20" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                                  <path d="M9 7V5H15V7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                                  <path d="M7 7L8 19H16L17 7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                                  <path d="M10 11V16" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                                  <path d="M14 11V16" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                                </svg>
                              </button>
                            </div>
                          </td>
                        </tr>

                        {isExpanded ? <SaleItemsList sale={sale} /> : null}
                      </Fragment>
                    );
                  })
                : null}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}
