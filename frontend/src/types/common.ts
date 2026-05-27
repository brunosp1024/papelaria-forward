export type UUID = string;
export type ISODateString = string;
export type DecimalString = string;


export interface AuditFields {
  created_at: ISODateString;
  updated_at: ISODateString;
  created_by: UUID | null;
  updated_by: UUID | null;
}