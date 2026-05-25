import UploadPage from "./UploadPage";
import AuditPage from "./AuditPage";

function Dashboard() {
  return (
    <div>
      <h1>Breathe ESG Dashboard</h1>

      <UploadPage />

      <hr />

      <AuditPage />
    </div>
  );
}

export default Dashboard;