import { useState } from "react";
import api from "../api";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [sourceType, setSourceType] = useState("SAP");

  const handleUpload = async () => {
    const formData = new FormData();

    formData.append("file", file);
    formData.append("source_type", sourceType);

    try {
      await api.post("upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert("Upload Successful");
    } catch (err) {
      console.error(err);
      alert("Upload Failed");
    }
  };

  return (
    <div>
      <select
        value={sourceType}
        onChange={(e) =>
          setSourceType(e.target.value)
        }
      >
        <option value="SAP">SAP</option>
        <option value="UTILITY">UTILITY</option>
        <option value="TRAVEL">TRAVEL</option>
      </select>

      <br />
      <br />

      <input
        type="file"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br />
      <br />

      <button onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
}

export default UploadForm;