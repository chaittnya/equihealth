import React, { useEffect, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";

import HeroSection from "../components/common/HeroSection";
import ChartHospitalCount from "../components/common/ChartHospitalCount";
import ChartBedCount from "../components/common/ChartBedCount";
import ChartBedsPerPopulation from "../components/common/ChartBedsPerPopulation";

import { setActivePage } from "../redux/features/activePageSlice";

const Home = () => {
  const dispatch = useDispatch();

  const { loaded } = useSelector((state) => state.healthInfra);
  const districts = useSelector((state) => state.healthInfra?.districts || {});
  const hospitals = useSelector((state) => state.healthInfra?.hospitals || {});

  useEffect(() => {
    dispatch(setActivePage(0));
  }, [dispatch]);

  const kpis = useMemo(() => {
    const districtsList = Object.values(districts.byId || {});
    const hospitalsById = hospitals.byId || {};

    const totalHospitals = districtsList.reduce(
      (sum, d) => sum + (d.hospitals?.length || 0),
      0
    );

    const totalBeds = districtsList.reduce(
      (sum, d) =>
        sum +
        (d.hospitals?.reduce(
          (s, hid) => s + (hospitalsById[hid]?.total_beds || 0),
          0
        ) || 0),
      0
    );

    const totalPopulation = districtsList.reduce(
      (sum, d) => sum + (d.total_persons || 0),
      0
    );

    const bedsPer10kPopulation = totalPopulation
      ? (totalBeds / totalPopulation) * 10000
      : 0;

    return {
      totalHospitals,
      totalBeds,
      avgBedsPer10k: bedsPer10kPopulation.toFixed(2),
    };
  }, [districts, hospitals]);

  return (
    <div id="home">
      <HeroSection />
      <div className="kpi-section">
        {!loaded ? (
          <p>Loading KPIs...</p>
        ) : kpis ? (
          <>
            <div className="kpi">
              <h3>Total Hospitals</h3>
              <p>{kpis.totalHospitals}</p>
            </div>
            <div className="kpi">
              <h3>Total Beds</h3>
              <p>{kpis.totalBeds}</p>
            </div>
            <div className="kpi">
              <h3>Avg Beds per 10,000 People</h3>
              <p>{kpis.avgBedsPer10k}</p>
            </div>
          </>
        ) : (
          <p>No KPI data available</p>
        )}
      </div>

      <div className="charts">
        <ChartHospitalCount />
        <ChartBedCount />
        <ChartBedsPerPopulation />
      </div>
    </div>
  );
};

export default Home;
