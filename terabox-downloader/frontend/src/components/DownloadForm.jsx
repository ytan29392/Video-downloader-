import React, { useState } from "react";

function DownloadForm({ onSubmit, loading }) {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState("mp4"); // default format

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url) return alert("Please enter a URL");
    onSubmit(url, format); // pass format along with URL
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter video or Terabox link"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "400px", padding: "0.5rem", marginRight: "1rem" }}
      />
      <select
        value={format}
        onChange={(e) => setFormat(e.target.value)}
        style={{ padding: "0.5rem" }}
      >
        <option value="mp4">Video (MP4)</option>
        <option value="mp3">Audio (MP3)</option>
      </select>
      <button
        type="submit"
        disabled={loading}
        style={{ marginLeft: "1rem", padding: "0.5rem 1rem" }}
      >
        {loading ? "Downloading..." : "Download"}
      </button>
    </form>
  );
}

export default DownloadForm;
