import "./CommissionsList.css"
import React, { useState } from "react";
import DateInput from "../../components/UI/DateInput";
import DataTable from "./components/DataTable";
import api from "../../api/client";

const CommissionsList = () => {
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [commissionsList, setCommissionsList] = useState([]);
    const [showDataTable, setShowDataTable] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const getCommissions = async () => {
        if (!startDate || !endDate || isLoading) {
            return;
        }

        setIsLoading(true);
        setShowDataTable(true);
        setErrorMessage("");

        // Converte Date para string yyyy-mm-dd
        const formatDate = (dateObj) =>
            dateObj ? dateObj.toISOString().slice(0, 10) : "";

        try {
            const response = await api.get('/commissions/summary', {
                params: {
                    start_date: formatDate(startDate),
                    end_date: formatDate(endDate)
                }
            });

            const data = Array.isArray(response.data) ? response.data : response.data?.results || [];
            const commissions = data.map((commission) => ({
                id: commission.seller_id || commission.seller?.id || commission.id,
                sellerCode: commission.seller_code || commission.seller?.code || "-",
                sellerName: commission.seller_name || commission.seller?.name || "-",
                salesTotal: commission.sales_count || commission.total_sales || 0,
                total: commission.commission_total || commission.total_commission || 0
            }));

            setCommissionsList(commissions);
        } catch (error) {
            setCommissionsList([]);
            setErrorMessage(error.message || "Erro ao carregar comissões.");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <section className="commissions-list">
            <header className="commissions-list__header">
                <div>
                    <h1 className="commissions-list__title">Comissões por vendedor</h1>
                    <p className="commissions-list__subtitle">Relatório de comissões dentro do período selecionado</p>
                </div>
            </header>

            <div className="commissions-list__toolbar">
                <span className="commissions-list__report-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M7 3H15L20 8V21H7V3Z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
                        <path d="M15 3V8H20" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
                        <path d="M10 17V13" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                        <path d="M13.5 17V10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                        <path d="M17 17V14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                    </svg>
                </span>

                <div className="commissions-list__filters" aria-label="Filtros do relatório">
                    <DateInput
                        label="Data inicial"
                        value={startDate}
                        onChange={setStartDate}
                        max={endDate || undefined}
                        placeholderText="Período de início"
                    />

                    <DateInput
                        label="Data final"
                        value={endDate}
                        onChange={setEndDate}
                        min={startDate || undefined}
                        placeholderText="Período de fim"
                    />

                    <button
                        className="commissions-list__search-button"
                        type="button"
                        disabled={!startDate || !endDate || isLoading}
                        onClick={getCommissions}
                        aria-label="Buscar comissões"
                        title="Buscar comissões"
                    >
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <circle cx="11" cy="11" r="6" stroke="currentColor" strokeWidth="2" />
                            <path d="M16 16L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                        </svg>
                    </button>
                </div>
            </div>

            <div className="commissions-list__content">
                {errorMessage ? <p className="commissions-list__error">{errorMessage}</p> : null}
                {!showDataTable && !errorMessage ? (
                    <p className="commissions-list__empty-state">Para visualizar o relatório, selecione um período nos campos acima.</p>
                ) : null}
                {commissionsList.length > 0 && !errorMessage ? (
                    <DataTable showDataTable={showDataTable && !errorMessage} commissionsList={commissionsList}/>
                ) : null}
            </div>
        </section>
    )

}

export default CommissionsList;
