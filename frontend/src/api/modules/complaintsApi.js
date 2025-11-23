import client from "../clients/client.js";

const endpoints = {
  postComplaint: "complaints",
  getComplaints: "complaints",
  getComplaintById: (complaintId) => `complaints/${complaintId}`,
};

const complaintsApi = {
  postComplaint: async ({
    firstName,
    lastName,
    phoneNumber,
    email,
    stateId,
    districtId,
    hospitalId,
    title,
    details,
    attachment,
  }) => {
    try {
      const formData = new FormData();
      formData.append(
        "name",
        lastName ? `${firstName} ${lastName}` : firstName
      );
      formData.append("phone_number", phoneNumber);
      formData.append("email", email);
      formData.append("state_id", stateId);
      formData.append("district_id", districtId);
      formData.append("hospital_id", hospitalId);
      formData.append("title", title);
      formData.append("details", details);
      if (attachment) formData.append("attachment", attachment);
      const res = await client.post(endpoints.postComplaint, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getComplaints: async ({
    stateId,
    districtId,
    hospitalId,
    search,
    page,
    pageSize,
    orderBy,
    orderDir,
  } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      if (districtId) params.district_id = districtId;
      if (hospitalId) params.hospital_id = hospitalId;
      if (search) params.search = search;
      if (page) params.page = page;
      if (pageSize) params.page_size = pageSize;
      if (orderBy) params.order_by = orderBy;
      if (orderDir) params.order_dir = orderDir;
      const res = await client.get(endpoints.getComplaints, { params });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getComplaintById: async ({ complaintId }) => {
    try {
      const res = await client.get(endpoints.getComplaintById(complaintId));
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default complaintsApi;
