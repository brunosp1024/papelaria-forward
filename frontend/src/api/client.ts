import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";


const baseURL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

type RetryableRequestConfig = InternalAxiosRequestConfig & {
  _retry?: boolean;
};

type ApiErrorPayload = {
  detail?: string;
  error?: string;
};

const api = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});

let refreshTokenRequest: Promise<void> | null = null;

async function refreshToken() {
  if (!refreshTokenRequest) {
    refreshTokenRequest = api.post("/token/refresh/", {}).then(() => undefined);
  }

  try {
    await refreshTokenRequest;
  } finally {
    refreshTokenRequest = null;
  }
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiErrorPayload>) => {
    const originalRequest = error.config as RetryableRequestConfig | undefined;
    const status = error.response?.status;
    const requestUrl = originalRequest?.url || "";
    const shouldSkipRefresh =
      requestUrl.includes("/token/") ||
      requestUrl.includes("/token/refresh/");

    if (status === 401 && originalRequest && !originalRequest._retry && !shouldSkipRefresh) {
      originalRequest._retry = true;

      try {
        await refreshToken();
        return api(originalRequest);
      } catch {
        // Falls through to normalized error message below.
      }
    }

    const message =
      error.response?.data?.detail ||
      error.response?.data?.error ||
      (error.message === "Network Error" ? "Nao foi possivel conectar ao servidor." : undefined) ||
      "Ocorreu um erro inesperado.";
    return Promise.reject(new Error(message));
  }
);

export default api;
