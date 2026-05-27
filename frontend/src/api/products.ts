import api from "./client";
import { Product, ProductInput, UUID } from "../types";
import { PaginatedResponse } from "./pagination";


export const productsApi = {
  list: (params?: Record<string, string>) =>
    api
      .get<PaginatedResponse<Product>>("/products/", { params })
      .then((r) => r.data),

  listAll: () =>
    api
      .get<PaginatedResponse<Product>>("/products/", {
          params: { page_size: 1000, ordering: "name" }
      })
      .then((r) => r.data.results),

  get: (id: UUID) =>
    api.get<Product>(`/products/${id}/`).then((r) => r.data),

  create: (data: ProductInput) =>
    api.post<Product>("/products/", data).then((r) => r.data),

  update: (id: UUID, data: ProductInput) =>
    api.put<Product>(`/products/${id}/`, data).then((r) => r.data),

  remove: (id: UUID) =>
    api.delete(`/products/${id}/`),
};