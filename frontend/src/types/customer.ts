import { AuditFields, UUID } from "./common";


export interface Customer extends AuditFields {
  id: UUID;
  name: string;
  email: string;
  phone: string | null;
}

export interface CustomerInput {
  name: string;
  email: string;
  phone?: string | null;
}