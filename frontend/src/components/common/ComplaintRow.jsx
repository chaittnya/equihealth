import React from "react";

const ComplaintRow = ({ complaint }) => {
  return (
    <div className="complaint-row grid">
      <div>{complaint.title}</div>
      <div>{complaint.district_name || "-"}</div>
      <div>{complaint.hospital_name || "-"}</div>
      <div>
        {complaint.created_at
          ? new Date(complaint.created_at).toLocaleString()
          : "-"}
      </div>
    </div>
  );
};

export default ComplaintRow;
