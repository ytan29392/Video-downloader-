import React, { useState } from "react";
import axios from "./services/api";
import DownloadForm from "./components/DownloadForm";

function App() {
  const [fileName, setFileName] = useState(""); // only store filename
  const [loading, setLoading] = useState(false);
  const [format, setFormat] = useState("mp4"); // store selected format

  const handleDownload = async (url, selectedFormat) => {
    setLoading(true);
    try {
      // Call backend with URL and format
      const res = await axios.get("/api/download/", { params: { url, format: selectedFormat } });

      // Extract just the filename from full path
      const path = res.data.file_path;
      const name = path.split("/").pop();
      setFileName(name);

    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        alert("Error: " + err.response.data.detail);
      } else {
        alert("Unknown error occurred: " + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1> Video (MPC4) and Audio(MPC3) Downloader</h1>
      <DownloadForm
        onSubmit={handleDownload}
        loading={loading}
        format={format}
        setFormat={setFormat} // pass down setter to allow format selection
      />

      {fileName && (
        <div style={{ marginTop: "1rem" }}>
          <strong>Download ready:</strong>{" "}
          <a
            href={`http://localhost:8000/files/${encodeURIComponent(fileName)}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            Click to download
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
