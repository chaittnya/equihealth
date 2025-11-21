import { createSlice } from "@reduxjs/toolkit";

import { capitalizeWords } from "../../utils/formatters";

export const healthInfraSlice = createSlice({
  name: "healthInfra",
  initialState: {
    districts: { byId: {}, allIds: [] },
    hospitals: { byId: {}, allIds: [] },
    loaded: false,
  },
  reducers: {
    setHealthInfra: (state, action) => {
      const { data } = action.payload;

      state.districts = { byId: {}, allIds: [] };
      state.hospitals = { byId: {}, allIds: [] };

      const { stateId } = data[0];

      data[0].districts.forEach((district) => {
        const districtId = district.district_id;

        const formattedDistrict = {
          ...district,
          district_name: capitalizeWords(district.district_name),
          state_id: stateId,
          hospitals: district.hospitals.map((h) => h.hospital_id),
        };

        state.districts.byId[districtId] = formattedDistrict;
        state.districts.allIds.push(districtId);

        district.hospitals.forEach((hospital) => {
          const hospitalId = hospital.hospital_id;

          const formattedHospital = {
            ...hospital,
            hospital_name: capitalizeWords(hospital.hospital_name),
            address: hospital.address ? capitalizeWords(hospital.address) : "",
            state_id: stateId,
            district_id: districtId,
          };

          state.hospitals.byId[hospitalId] = formattedHospital;
          state.hospitals.allIds.push(hospitalId);
        });
      });

      state.loaded = true;
    },
  },
});

export const { setHealthInfra } = healthInfraSlice.actions;

export default healthInfraSlice.reducer;
