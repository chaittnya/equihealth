import axios from "axios";

const baseURL = import.meta.env.VITE_BACKEND_URL;

// 🔒 If page is https and baseURL is http -> upgrade to https
if (typeof window !== "undefined") {
  const isHttpsPage = window.location.protocol === "https:";
  if (isHttpsPage && baseURL.startsWith("http://")) {
    baseURL = baseURL.replace(/^http:\/\//, "https://");
  }
}

// TEMP: log to verify what is actually used in the deployed app
console.log("AXIOS BASE URL: ", baseURL);

const client = axios.create({
  baseURL,
  paramsSerializable: {
    serialize: (params) => {
      const searchParams = new URLSearchParams();
      Object.keys(params).forEach((key) => {
        searchParams.append(key, params[key]);
      });
      return searchParams.toString();
    },
  },
});

client.interceptors.request.use(async (config) => {
  const method = (config.method || "get").toLowerCase();
  config.headers = config.headers || {};
  if (["post", "put", "patch", "delete"].includes(method)) {
    config.headers["Content-Type"] = "application/json";
  }
  return {
    ...config,
  };
});

client.interceptors.response.use(
  async (response) => {
    if (response?.data) return response.data;
    return response;
  },
  (error) => {
    const message = error?.response?.data?.message;
    if (message) throw message || "Something went wrong. Please try again.";
    throw error;
  }
);

export default client;
