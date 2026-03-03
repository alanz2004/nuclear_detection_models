import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI server URL
  withCredentials: true,            // optional, for cookies if needed
});

// Optional: attach auth token if you have login
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;