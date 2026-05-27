import api from "./client";
import { Customer, CustomerInput, UUID } from "../types";
import { PaginatedResponse } from "./pagination";


export const customersApi = {
  list: (params?: Record<string, string>) =>
    api
      .get<PaginatedResponse<Customer>>("/customers/", { params })
      .then((r) => r.data),

  listAll: () =>
    api
      .get<PaginatedResponse<Customer>>("/customers/", {
          params: { page_size: 1000, ordering: "name" }
      })
      .then((r) => r.data.results),

  get: (id: UUID) =>
    api.get<Customer>(`/customers/${id}/`).then((r) => r.data),

  create: (data: CustomerInput) =>
    api.post<Customer>("/customers/", data).then((r) => r.data),

  update: (id: UUID, data: CustomerInput) =>
    api.put<Customer>(`/customers/${id}/`, data).then((r) => r.data),

  remove: (id: UUID) =>
    api.delete(`/customers/${id}/`),
};