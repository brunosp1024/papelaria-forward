import "./DataTable.css"
import { formatCurrency } from "../../../utils/formatCurrency"


const DataTable = ({commissionsList, showDataTable}) => {
    return (
        <div className={`table-commissions table-responsive ${showDataTable ? '' : 'd-none'}`}>
            <table className='table-commissions__table'>
                <colgroup>
                    <col className="table-commissions__code-column" />
                    <col className="table-commissions__seller-column" />
                    <col className="table-commissions__seller-column" />
                    <col className="table-commissions__sales-column" />
                    <col className="table-commissions__total-column" />
                </colgroup>
                <thead>
                    <tr>
                        <th>Cód</th>
                        <th colSpan={2}>Vendedor</th>
                        <th colSpan={2}>Total de vendas</th>
                        <th>Total de comissões</th>
                    </tr>
                </thead>
                <tbody>
                    {commissionsList.length ? commissionsList.map(commission => {
                        return (
                            <tr key={commission.id}>
                                <td>{commission.sellerCode}</td>
                                <td colSpan={2}>{commission.sellerName}</td>
                                <td colSpan={2}>{commission.salesTotal}</td>
                                <td>{formatCurrency(commission.total)}</td>
                            </tr>
                        )
                        }) : <tr><td className="py-4 text-center" colSpan={6}>Lista vazia</td></tr>
                    }
                </tbody>
                {commissionsList.length ?
                    <tfoot>
                        <tr>
                            <th colSpan={2} style={{ textAlign: 'left' }}>Total de comissões do período</th>
                            <th colSpan={3}></th>
                            <th style={{ textAlign: 'center' }}>{formatCurrency(commissionsList.reduce((total, c) => {return total + parseFloat(c.total || 0)}, 0))}</th>
                        </tr>
                    </tfoot> : null
                }
            </table>
        </div>
    )
}

export default DataTable;
