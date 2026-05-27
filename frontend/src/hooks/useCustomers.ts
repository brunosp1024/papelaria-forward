import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { customersApi } from "../api";
import { CustomerInput, UUID } from "../types";
import { customerKeys } from "./queryKeys";


export function useCustomers(params?: Record<string, string>) {
  return useQuery({
    queryKey: customerKeys.list(params),
    queryFn: () => customersApi.list(params),
  });
}

export function useAllCustomers() {
  return useQuery({
    queryKey: [...customerKeys.lists(), "all"],
    queryFn: () => customersApi.listAll(),
  });
}

export function useCustomer(id?: UUID) {
  return useQuery({
    queryKey: id ? customerKeys.detail(id) : [...customerKeys.details(), "empty"],
    queryFn: () => customersApi.get(id as UUID),
    enabled: Boolean(id),
  });
}

export function useCreateCustomer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CustomerInput) => customersApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: customerKeys.lists() });
    },
  });
}

export function useUpdateCustomer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: UUID; data: CustomerInput }) => customersApi.update(id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: customerKeys.lists() });
      queryClient.invalidateQueries({ queryKey: customerKeys.detail(variables.id) });
    },
  });
}

export function useDeleteCustomer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: UUID) => customersApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: customerKeys.lists() });
    },
  });
}
