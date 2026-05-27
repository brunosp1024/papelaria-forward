import api from "./client";
import { Commission } from "../types";
import { PaginatedResponse } from "./pagination";


export const commissionsApi = {
  list: (params?: Record<string, string>) =>
    api
      .get<PaginatedResponse<Commission>>("/commissions/", { params })
      .then((r) => r.data),
};