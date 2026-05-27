import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { sellersApi } from "../api";
import { SellerInput, UUID } from "../types";
import { sellerKeys } from "./queryKeys";


export function useSellers(params?: Record<string, string>) {
  return useQuery({
    queryKey: sellerKeys.list(params),
    queryFn: () => sellersApi.list(params),
  });
}

export function useAllSellers() {
  return useQuery({
    queryKey: [...sellerKeys.lists(), "all"],
    queryFn: () => sellersApi.listAll(),
  });
}

export function useSeller(id?: UUID) {
  return useQuery({
    queryKey: id ? sellerKeys.detail(id) : [...sellerKeys.details(), "empty"],
    queryFn: () => sellersApi.get(id as UUID),
    enabled: Boolean(id),
  });
}

export function useCreateSeller() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SellerInput) => sellersApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sellerKeys.lists() });
    },
  });
}

export function useUpdateSeller() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: UUID; data: SellerInput }) => sellersApi.update(id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: sellerKeys.lists() });
      queryClient.invalidateQueries({ queryKey: sellerKeys.detail(variables.id) });
    },
  });
}

export function useDeleteSeller() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: UUID) => sellersApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sellerKeys.lists() });
    },
  });
}
