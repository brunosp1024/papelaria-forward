import api from "./client";
import { CommissionReportResponse } from "../types";
import { PaginatedResponse } from "./pagination";


export const commissionsApi = {
  list: (params?: Record<string, string>) =>
    api
      .get<CommissionReportResponse>("/commissions/summary", { params })
      .then((r) => r.data),
};