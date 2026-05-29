import { DecimalString, UUID } from "./common";
import { Seller } from "./seller";

export interface CommissionReportItem {
  seller: Seller;
  total_sales: number;
  total_commission: DecimalString;
}

export type CommissionReportResponse = CommissionReportItem[];
