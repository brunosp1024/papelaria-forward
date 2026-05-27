import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { salesApi } from "../api";
import { SaleInput, UUID } from "../types";
import { saleKeys } from "./queryKeys";


export function useSales(params?: Record<string, string>) {
  return useQuery({
    queryKey: saleKeys.list(params),
    queryFn: () => salesApi.list(params),
  });
}

export function useAllSales() {
  return useQuery({
    queryKey: [...saleKeys.lists(), "all"],
    queryFn: () => salesApi.listAll(),
  });
}

export function useSale(id?: UUID) {
  return useQuery({
    queryKey: id ? saleKeys.detail(id) : [...saleKeys.details(), "empty"],
    queryFn: () => salesApi.get(id as UUID),
    enabled: Boolean(id),
  });
}

export function useCreateSale() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SaleInput) => salesApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: saleKeys.lists() });
    },
  });
}

export function useUpdateSale() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: UUID; data: SaleInput }) => salesApi.update(id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: saleKeys.lists() });
      queryClient.invalidateQueries({ queryKey: saleKeys.detail(variables.id) });
    },
  });
}

export function useDeleteSale() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: UUID) => salesApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: saleKeys.lists() });
    },
  });
}
