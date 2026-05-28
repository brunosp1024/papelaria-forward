import { FormEvent, useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  useAllCustomers, useAllSellers, useAllProducts,
  useCreateSale, useSale, useUpdateSale,
} from "../../hooks";
import { Customer, Product, SaleInput, SaleItemInput, SaleItem, Seller, UUID } from "../../types";
import { formatCurrency } from "../../utils/formatCurrency";
import AddSaleItem from "./components/AddSaleItem";
import "./SalesForm.css";
import { useToast } from "../../components/UI/ToastContext";
import { toInputValue, toDisplayValue } from "../../utils/dateUtils";


// ─── Initial state of the form ──────────────────────────────────────
const INITIAL_STATE: SaleInput = {
  datetime: toInputValue(new Date()),
  seller: "",
  customer: "",
  items: [],
};

// ─── Auxiliary component for page state ─────────────
function PageState({ message, isError }: { message: string; isError?: boolean }) {
  return (
    <section className="sales-form">
      <p className={`sales-form__state${isError ? " sales-form__state--error" : ""}`}>
        {message}
      </p>
    </section>
  );
}

// ─── Main component ─────────────────────────────────
export default function SalesForm() {
  const { showToast } = useToast();
  const navigate = useNavigate();
  const { id } = useParams<{ id: UUID }>();
  const isEditing = Boolean(id);

  // ── Grouped hooks ──
  const saleQuery      = useSale(id);
  const sellersQuery   = useAllSellers();
  const customersQuery = useAllCustomers();
  const productsQuery  = useAllProducts();
  const createSale     = useCreateSale();
  const updateSale     = useUpdateSale();

  const [form, setForm]           = useState<SaleInput>(INITIAL_STATE);
  const [formError, setFormError] = useState("");

  const productMap = useMemo(
    () => new Map<UUID, Product>(productsQuery.data?.map((p: Product) => [p.id, p])),
    [productsQuery.data]
  );

  // Fill the form when editing
  useEffect(() => {
    if (!saleQuery.data) return;
    const { datetime, seller, customer, items } = saleQuery.data;
    setForm({
      datetime: toInputValue(new Date(datetime)),
      seller: seller.id,
      customer: customer.id,
      items: items.map((item: SaleItem) => ({
        product: item.product.id,
        quantity: item.quantity,
      })),
    });
  }, [saleQuery.data]);

  // Helper to update form fields
  const setField = <K extends keyof SaleInput>(key: K, value: SaleInput[K]) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  // Derived totals
  const totalValue = useMemo(
    () => form.items.reduce((sum, { product, quantity }) => {
      const unitValue = Number(productMap.get(product)?.unit_value ?? 0);
      return sum + unitValue * quantity;
    }, 0),
    [form.items, productMap]
  );

  // Handlers for items
  const handleAddItem = (item: SaleItemInput) => {
    setField("items", [...form.items, item]);
    setFormError("");
  };

  const handleRemoveItem = (productId: UUID) =>
    setField("items", form.items.filter((i) => i.product !== productId));

  // Submit
  const isSaving  = createSale.isPending || updateSale.isPending;
  const canSubmit = form.seller && form.customer && form.items.length > 0 && !isSaving;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) {
      setFormError("Preencha os dados da venda e adicione pelo menos um produto.");
      return;
    }

    const payload = {
      datetime: new Date(form.datetime).toISOString(),
      seller: form.seller,
      customer: form.customer,
      items: form.items.map(({ product, quantity }) => ({ product, quantity })),
    };

    try {
      const message = id ? "Venda atualizada com sucesso!" : "Venda criada com sucesso!";
      await (id
        ? updateSale.mutateAsync({ id, data: payload })
        : createSale.mutateAsync(payload));
      showToast(message, "success");
      navigate("/vendas");
    } catch (error) {
      setFormError(error instanceof Error ? error.message : "Não foi possível salvar a venda.");
    }
  }

  // Early returns for loading/error states
  if (isEditing && saleQuery.isPending) return <PageState message="Carregando venda..." />;
  if (isEditing && saleQuery.isError)   return <PageState message="Erro ao carregar venda." isError />;

  return (
    <section className="sales-form">
      <header className="sales-form__header">
        <div>
          <h1 className="sales-form__title">{isEditing ? "Alterar venda" : "Nova venda"}</h1>
          <p className="sales-form__subtitle">
            {isEditing
              ? `Nota Fiscal ${saleQuery.data?.invoice_number ?? ""}`
              : "Cadastro de venda"}
          </p>
        </div>
        <Link className="sales-form__back-link" to="/vendas">Voltar</Link>
      </header>

      <form className="sales-form__grid" onSubmit={handleSubmit}>

        {/* ── Products panel ── */}
        <div className="sales-form__panel sales-form__panel--products">
          <div className="sales-form__section-heading">
            <div>
              <h2>Produtos</h2>
              <span>
                {form.items.length === 0
                  ? "Nenhum item adicionado"
                  : form.items.length === 1
                  ? "1 item adicionado"
                  : `${form.items.length} itens adicionados`}
              </span>
            </div>
          </div>

          <AddSaleItem
            selectedProductIds={form.items.map((i) => i.product)}
            onAddItem={handleAddItem}
          />

          <div className="sales-form__items-wrapper">
            <table className="sales-form__items-table">
              <thead>
                <tr>
                  <th>Produto/Serviço</th>
                  <th>Quantidade</th>
                  <th>Preço unitário</th>
                  <th>Total</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {form.items.length > 0 ? (
                  form.items.map(({ product, quantity }) => {
                    const p = productMap.get(product);
                    const unitValue = Number(p?.unit_value ?? 0);
                    return (
                      <tr key={product}>
                        <td>
                          <strong>{p?.description}</strong>
                          <span>{p?.code}</span>
                        </td>
                        <td>{quantity}</td>
                        <td>{formatCurrency(unitValue)}</td>
                        <td>{formatCurrency(unitValue * quantity)}</td>
                        <td>
                          <button
                            className="sales-form__remove-button"
                            type="button"
                            onClick={() => handleRemoveItem(product)}
                            aria-label={`Remover ${p?.description}`}
                          >
                            Remover
                          </button>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td className="sales-form__empty" colSpan={5}>
                      Nenhum produto adicionado.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>


        {/* ── Summary panel ── */}
        <aside className="sales-form__panel sales-form__panel--summary">
          <div className="sales-form__section-heading">
            <div>
              <h2>Dados da venda</h2>
              <span>{toDisplayValue(new Date(form.datetime).toISOString())}</span>
            </div>
          </div>

          <div className="sales-form__fields">
            <label className="sales-form__field">
              <span>Vendedor</span>
              <select value={form.seller} onChange={(e) => setField("seller", e.target.value)} required>
                <option value="">Selecione...</option>
                {sellersQuery.data?.map((seller: Seller) => (
                  <option key={seller.id} value={seller.id}>{seller.name}</option>
                ))}
              </select>
            </label>

            <label className="sales-form__field">
              <span>Cliente</span>
              <select value={form.customer} onChange={(e) => setField("customer", e.target.value)} required>
                <option value="">Selecione...</option>
                {customersQuery.data?.map((customer: Customer) => (
                  <option key={customer.id} value={customer.id}>{customer.name}</option>
                ))}
              </select>
            </label>
          </div>

          <div className="sales-form__total-box">
            <span>Valor total da venda</span>
            <strong>{formatCurrency(totalValue)}</strong>
          </div>

          {formError && <p className="sales-form__error">{formError}</p>}

          <div className="sales-form__actions">
            <Link className="sales-form__cancel-button" to="/vendas">Cancelar</Link>
            <button className="sales-form__submit-button" type="submit" disabled={!canSubmit}>
              {isSaving ? "Salvando..." : "Finalizar"}
            </button>
          </div>
        </aside>

      </form>
    </section>
  );
}