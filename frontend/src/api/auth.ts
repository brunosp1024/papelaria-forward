import api from "./client";

export type LoginPayload = {
  username: string;
  password: string;
};

export const authApi = {
  login: (data: LoginPayload) =>
    api.post<{ detail: string }>("/token/", data).then((r) => r.data),

  refresh: (signal?: AbortSignal) =>
    api.post<{ detail: string }>("/token/refresh/", {}, { signal }).then((r) => r.data),

  logout: () => api.post<{ detail: string }>("/logout/", {}).then((r) => r.data),
};