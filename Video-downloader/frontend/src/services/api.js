import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // backend API
  timeout: 30000, // optional timeout
});

// Function to call backend download endpoint
export const downloadVideo = async (url) => {
  try {
    const res = await api.get("/api/download/", { params: { url } });

    // Extract filename from full backend file path
    const filePath = res.data.file_path;
    const fileName = filePath.split("/").pop();

    // Return filename for frontend to build download link
    return { fileName };
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      throw new Error(err.response.data.detail);
    } else {
      throw new Error(err.message || "Unknown error occurred");
    }
  }
};

export default api;
