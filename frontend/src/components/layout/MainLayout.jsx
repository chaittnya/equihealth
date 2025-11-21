import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { Outlet } from "react-router-dom";

import hospitalsApi from "../../api/modules/hospitalsApi.js";

import NavBar from "../common/Navbar";
import Footer from "../common/Footer";

import { setHealthInfra } from "../../redux/features/healthInfraSlice.js";

const MainLayout = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchHospitalInfra = async () => {
      const { res, err } = await hospitalsApi.getHospitalsGrouped({ stateId: 18 });
      if (res) dispatch(setHealthInfra(res));
      else if (err) console.log(err);
    };
    
    fetchHospitalInfra();
  }, [dispatch]);

  return (
    <>
      <NavBar />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  );
};

export default MainLayout;
