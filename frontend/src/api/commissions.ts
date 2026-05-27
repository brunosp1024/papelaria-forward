import api from "./client";
import { Commission, CommissionInput, UUID } from "../types";
import { PaginatedResponse } from "./pagination";


export const commissionsApi = {
  list: (params?: Record<string, string>) =>
    api
      .get<PaginatedResponse<Commission>>("/commission-configs/", { params })
      .then((r) => r.data),

  listAll: () =>
    api
      .get<PaginatedResponse<Commission>>("/commission-configs/",{
          params: { page_size: 1000, ordering: "name" }
      })
      .then((r) => r.data.results),

  get: (id: UUID) =>
    api.get<Commission>(`/commission-configs/${id}/`).then((r) => r.data),

  create: (data: CommissionInput) =>
    api.post<Commission>("/commission-configs/", data).then((r) => r.data),

  update: (id: UUID, data: CommissionInput) =>
    api.put<Commission>(`/commission-configs/${id}/`, data).then((r) => r.data),

  remove: (id: UUID) =>
    api.delete(`/commission-configs/${id}/`),
};

// Backward-compatible alias for common misspelling.
export const commisionsApi = commissionsApi;