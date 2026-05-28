import { useMemo } from "react";
import { Sale } from "../../../types";
import "./SaleItemsList.css";
import { formatCurrency } from "../../../utils/formatCurrency";

export function SaleItemsList({ sale }: { sale: Sale }) {
  const totalQuantity = useMemo(
    () => sale.items.reduce((sum, item) => sum + item.quantity, 0),
    [sale.items],
  );

  return (
    <>
      <tr className="sales-list__child-row">
        <td colSpan={6}>
          <div className="sales-list__child-wrapper">
            <table className="sales-list__table sales-list__table--child">
              <thead>
                <tr>
                  <th>Produto/Servico</th>
                  <th>Quantidade</th>
                  <th>Preco unitario</th>
                  <th>Total do produto</th>
                  <th>% de comissao</th>
                  <th>Comissao</th>
                </tr>
              </thead>
              <tbody>
                {sale.items.length > 0 ? (
                  sale.items.map((item) => (
                    <tr key={item.id}>
                      <td>{item.product.description}</td>
                      <td>{item.quantity}</td>
                      <td>{formatCurrency(item.product.unit_value)}</td>
                      <td>{formatCurrency(item.subtotal)}</td>
                      <td>{String(item.product.commission_percentage).replace(".", ",")}%</td>
                      <td>{formatCurrency(item.commission_value)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td className="sales-list__empty-inline" colSpan={6}>
                      Lista vazia
                    </td>
                  </tr>
                )}

                {sale.items.length > 0 ? (
                  <tr className="sales-list__totals-row">
                    <th>Total venda</th>
                    <th colSpan={2}>{totalQuantity}</th>
                    <th colSpan={2}>{formatCurrency(sale.total_value)}</th>
                    <th>{formatCurrency(sale.total_commission)}</th>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
        </td>
      </tr>
    </>
  );
}
