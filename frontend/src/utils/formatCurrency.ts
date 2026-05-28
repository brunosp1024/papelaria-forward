// Utilitário global para formatação de moeda (BRL)
export function formatCurrency(value: string | number) {
  const currencyFormatter = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
  return currencyFormatter.format(Number(value || 0));
}
