import React, { useEffect } from "react";
import { useDispatch } from "react-redux";

import { setActivePage } from "../redux/features/activePageSlice";

const ComplaintHistory = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(setActivePage(2));
  }, [dispatch]);

  return <div id="complaints-list"></div>;
};

export default ComplaintHistory;
