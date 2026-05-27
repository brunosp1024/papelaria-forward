import { AuditFields, DecimalString, UUID } from "./common";


export interface Product extends AuditFields {
  id: UUID;
  code: string;
  description: string;
  unit_value: DecimalString;
  commission_percentage: DecimalString;
}

export interface ProductInput {
  code: string;
  description: string;
  unit_value: DecimalString;
  commission_percentage: DecimalString;
}