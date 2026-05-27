import axios from "axios";


const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.error ||
      "Ocorreu um erro inesperado.";
    return Promise.reject(new Error(message));
  }
);

export default api;