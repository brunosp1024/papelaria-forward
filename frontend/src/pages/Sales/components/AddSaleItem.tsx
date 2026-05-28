import { useMemo, useState } from "react";
import SelectSearch, { SelectSearchOption } from "../../../components/UI/SelectSearch";

import { useAllProducts } from "../../../hooks";
import { Product, UUID } from "../../../types";
import { formatCurrency } from "../../../utils/formatCurrency";

type AddSaleItemProps = {
  selectedProductIds: UUID[];
  onAddItem: (item: { product: UUID; quantity: number }) => void;
};

export default function AddSaleItem({ selectedProductIds, onAddItem }: AddSaleItemProps) {
  const productsQuery = useAllProducts();
  const [productId, setProductId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState("");

  const availableProducts = useMemo<Product[]>(
    () => (productsQuery.data ?? []).filter((product: Product) => !selectedProductIds.includes(product.id)),
    [productsQuery.data, selectedProductIds],
  );

  const selectedProduct = availableProducts.find((product) => product.id === productId);
  const previewTotal = selectedProduct ? Number(selectedProduct.unit_value) * quantity : 0;
  const canAdd = Boolean(selectedProduct) && quantity > 0;

  function handleProductSelect(option: SelectSearchOption | null) {
    if (option) {
      setProductId(option.value);
      setError("");
    } else {
      setProductId("");
    }
  }

  function handleAddItem() {
    setError("");

    if (!selectedProduct || quantity <= 0) {
      setError("Selecione um produto e informe uma quantidade valida.");
      return;
    }

    onAddItem({ product: selectedProduct.id, quantity });
    setProductId("");
    setQuantity(1);
  }

  return (
    <div className="add-sale-item">
      <div className="add-sale-item__fields">
        <div className="sales-form__field add-sale-item__product">
          <span>Buscar pelo codigo ou descricao</span>
          <SelectSearch
            value={productId}
            onChange={handleProductSelect}
            options={availableProducts.map((product) => ({
              value: product.id,
              label: `${product.code} - ${product.description}`,
              unit_value: product.unit_value,
            }))}
            placeholder={productsQuery.isPending ? "Carregando produtos..." : "Digite o codigo ou a descricao"}
            loading={productsQuery.isPending}
            disabled={productsQuery.isPending}
            getOptionLabel={(option) => `${option.label}  ${option.unit_value ? `- ${formatCurrency(option.unit_value)}` : ""}`}
            getOptionValue={(option) => option.value}
            noResultsText="Nenhum produto encontrado."
          />
        </div>

        <label className="sales-form__field add-sale-item__quantity">
          <span>Quantidade</span>
          <input
            type="number"
            min="1"
            step="1"
            value={quantity}
            onChange={(event) => setQuantity(Number(event.target.value))}
          />
        </label>

        <div className="add-sale-item__preview">
          <span>Total do item</span>
          <strong>{formatCurrency(previewTotal)}</strong>
        </div>

        <button className="add-sale-item__button" type="button" onClick={handleAddItem} disabled={!canAdd}>
          Adicionar
        </button>
      </div>

      {productsQuery.isError ? <p className="sales-form__error">Erro ao carregar produtos.</p> : null}
      {error ? <p className="sales-form__error">{error}</p> : null}
    </div>
  );
}
