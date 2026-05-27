import { useQuery } from "@tanstack/react-query";

import { commissionsApi } from "../api";
import { commissionKeys } from "./queryKeys";


export function useCommissions(params?: Record<string, string>) {
  return useQuery({
    queryKey: commissionKeys.list(params),
    queryFn: () => commissionsApi.list(params),
  });
}
