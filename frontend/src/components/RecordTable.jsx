import { useEffect, useState } from "react";
import api from "../api";

function RecordTable() {
  const [records, setRecords] = useState([]);

  const fetchRecords = async () => {
    try {
      const response = await api.get("records/");
      setRecords(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const updateStatus = async (
    id,
    status
  ) => {
    try {
      await api.patch(
        `records/${id}/`,
        {
          status: status,
        }
      );

      fetchRecords();
    } catch (error) {
      console.error(error);
      alert("Update failed");
    }
  };

  return (
    <table border="1" cellPadding="10">
      <thead>
        <tr>
          <th>ID</th>
          <th>Category</th>
          <th>Scope</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        {records.map((record) => (
          <tr key={record.id}>
            <td>{record.id}</td>
            <td>{record.category}</td>
            <td>{record.scope}</td>
            <td>{record.status}</td>

            <td>
              <button
                onClick={() =>
                  updateStatus(
                    record.id,
                    "APPROVED"
                  )
                }
              >
                Approve
              </button>

              {" "}

              <button
                onClick={() =>
                  updateStatus(
                    record.id,
                    "REJECTED"
                  )
                }
              >
                Reject
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default RecordTable;