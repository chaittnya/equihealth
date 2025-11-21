import client from "../clients/client.js";

const endpoints = {
  getHospitalsGrouped: "hospitals/grouped",
};

const hospitalsApi = {
  getHospitalsGrouped: async ({ stateId, districtId } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      if (districtId) params.district_id = districtId;
      const res = await client.get(endpoints.getHospitalsGrouped, { params });
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default hospitalsApi;
