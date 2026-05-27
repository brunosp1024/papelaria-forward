import { UUID } from "../types";


export const customerKeys = {
  all: ["customers"] as const,
  lists: () => [...customerKeys.all, "list"] as const,
  list: (params?: Record<string, string>) => [...customerKeys.lists(), params ?? {}] as const,
  details: () => [...customerKeys.all, "detail"] as const,
  detail: (id: UUID) => [...customerKeys.details(), id] as const,
};

export const sellerKeys = {
  all: ["sellers"] as const,
  lists: () => [...sellerKeys.all, "list"] as const,
  list: (params?: Record<string, string>) => [...sellerKeys.lists(), params ?? {}] as const,
  details: () => [...sellerKeys.all, "detail"] as const,
  detail: (id: UUID) => [...sellerKeys.details(), id] as const,
};

export const productKeys = {
  all: ["products"] as const,
  lists: () => [...productKeys.all, "list"] as const,
  list: (params?: Record<string, string>) => [...productKeys.lists(), params ?? {}] as const,
  details: () => [...productKeys.all, "detail"] as const,
  detail: (id: UUID) => [...productKeys.details(), id] as const,
};

export const saleKeys = {
  all: ["sales"] as const,
  lists: () => [...saleKeys.all, "list"] as const,
  list: (params?: Record<string, string>) => [...saleKeys.lists(), params ?? {}] as const,
  details: () => [...saleKeys.all, "detail"] as const,
  detail: (id: UUID) => [...saleKeys.details(), id] as const,
};

export const commissionKeys = {
  all: ["commissions"] as const,
  lists: () => [...commissionKeys.all, "list"] as const,
  list: (params?: Record<string, string>) => [...commissionKeys.lists(), params ?? {}] as const,
};
