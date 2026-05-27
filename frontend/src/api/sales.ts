import api from "./client";
import { Sale, SaleInput, UUID } from "../types";
import { PaginatedResponse } from "./pagination";


export const salesApi = {
  list: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<Sale>>("/sales/", { params }).then((r) => r.data),

  listAll: () =>
    api
      .get<PaginatedResponse<Sale>>("/sales/", {
          params: { page_size: 1000, ordering: "name" }
      })
      .then((r) => r.data.results),

  get: (id: UUID) =>
    api.get<Sale>(`/sales/${id}/`).then((r) => r.data),

  create: (data: SaleInput) =>
    api.post<Sale>("/sales/", data).then((r) => r.data),

  update: (id: UUID, data: SaleInput) =>
    api.put<Sale>(`/sales/${id}/`, data).then((r) => r.data),

  remove: (id: UUID) =>
    api.delete(`/sales/${id}/`),
};