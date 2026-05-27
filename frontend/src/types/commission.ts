import { DecimalString, UUID } from "./common";
import { Seller } from "./seller";

export type Weekday = 0 | 1 | 2 | 3 | 4 | 5 | 6;

export interface Commission {
  id: UUID;
  day_of_week: Weekday;
  day_of_week_display: string;
  min_percentage: DecimalString;
  max_percentage: DecimalString;
}

export interface CommissionInput {
  day_of_week: Weekday;
  min_percentage: DecimalString;
  max_percentage: DecimalString;
}

export interface CommissionReportItem {
  seller: Seller;
  total_commission: DecimalString;
}

export type CommissionReportResponse = CommissionReportItem[];
 
export interface CommissionReportParams {
  start_date: string; // YYYY-MM-DD
  end_date: string;   // YYYY-MM-DD
}