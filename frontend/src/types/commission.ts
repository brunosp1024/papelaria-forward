import { DecimalString, UUID } from "./common";

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