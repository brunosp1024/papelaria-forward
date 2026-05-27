import { AuditFields, UUID } from "./common";


export interface Seller extends AuditFields {
  id: UUID;
  name: string;
  email: string;
  phone: string | null;
}

export interface SellerInput {
  name: string;
  email: string;
  phone?: string | null;
}