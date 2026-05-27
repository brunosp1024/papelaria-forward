import api from "./client";
import { Seller, SellerInput, UUID } from "../types";
import { PaginatedResponse } from "./pagination";


export const sellersApi = {
  list: (params?: Record<string, string>) =>
    api
      .get<PaginatedResponse<Seller>>("/sellers/", { params })
      .then((r) => r.data),

  listAll: () =>
    api
      .get<PaginatedResponse<Seller>>("/sellers/", {
          params: { page_size: 1000, ordering: "name" }
      })
      .then((r) => r.data.results),

  get: (id: UUID) =>
    api.get<Seller>(`/sellers/${id}/`).then((r) => r.data),

  create: (data: SellerInput) =>
    api.post<Seller>("/sellers/", data).then((r) => r.data),

  update: (id: UUID, data: SellerInput) =>
    api.put<Seller>(`/sellers/${id}/`, data).then((r) => r.data),

  remove: (id: UUID) =>
    api.delete(`/sellers/${id}/`),
};