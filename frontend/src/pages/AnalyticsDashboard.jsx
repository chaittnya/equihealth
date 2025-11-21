import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";

import Map from "../components/common/Map.jsx";
import SelectFilters from "../components/common/SelectFilters.jsx";

import { setActivePage } from "../redux/features/activePageSlice.js";

const AnalyticsDashboard = () => {
  const dispatch = useDispatch()

  const [selected, setSelected] = useState({
    district: null,
    hospital: null,
  });

  useEffect(() => {
    dispatch(setActivePage(1))
  }, [dispatch])

  return (
    <div id="analytics-dashboard">
      <SelectFilters selected={selected} setSelected={setSelected} />
      <Map selected={selected} />
    </div>
  );
};

export default AnalyticsDashboard;
