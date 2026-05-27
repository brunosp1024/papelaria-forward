import { DecimalString, UUID } from "./common";
import { Product } from "./product";


export interface SaleItem {
  id: UUID;
  product: Product;
  quantity: number;
  subtotal: DecimalString;
  commission_value: DecimalString;
}

export interface SaleItemInput {
  product: UUID;
  quantity: number;
}