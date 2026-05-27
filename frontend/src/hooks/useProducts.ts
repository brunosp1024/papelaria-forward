import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { productsApi } from "../api";
import { ProductInput, UUID } from "../types";
import { productKeys } from "./queryKeys";


export function useProducts(params?: Record<string, string>) {
  return useQuery({
    queryKey: productKeys.list(params),
    queryFn: () => productsApi.list(params),
  });
}

export function useAllProducts() {
  return useQuery({
    queryKey: [...productKeys.lists(), "all"],
    queryFn: () => productsApi.listAll(),
  });
}

export function useProduct(id?: UUID) {
  return useQuery({
    queryKey: id ? productKeys.detail(id) : [...productKeys.details(), "empty"],
    queryFn: () => productsApi.get(id as UUID),
    enabled: Boolean(id),
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ProductInput) => productsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
    },
  });
}

export function useUpdateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: UUID; data: ProductInput }) => productsApi.update(id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
      queryClient.invalidateQueries({ queryKey: productKeys.detail(variables.id) });
    },
  });
}

export function useDeleteProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: UUID) => productsApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: productKeys.lists() });
    },
  });
}
