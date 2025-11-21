import client from "../clients/client.js";

const endpoints = {
  getDistricts: "districts",
};

const districtsApi = {
  getDistricts: async ({ stateId } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      const res = await client.get(endpoints.getDistricts, { params });
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default districtsApi;
