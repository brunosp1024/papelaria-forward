import { AuditFields, DecimalString, ISODateString, UUID } from "./common";
import { Customer } from "./customer";
import { Seller } from "./seller";
import { SaleItem, SaleItemInput } from "./saleItem";

export interface Sale extends AuditFields {
  id: UUID;
  invoice_number: string;
  datetime: ISODateString;
  customer: Customer;
  seller: Seller;
  items: SaleItem[];
  total_value: DecimalString;
  total_commission: DecimalString;
}

export interface SaleInput {
  invoice_number: string;
  datetime: ISODateString;
  customer: UUID;
  seller: UUID;
  items: SaleItemInput[];
}