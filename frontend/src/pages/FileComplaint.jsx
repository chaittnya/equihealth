import React, { useEffect } from "react";
import { useDispatch } from "react-redux";

import ComplaintForm from "../components/common/ComplaintForm";

import { setActivePage } from "../redux/features/activePageSlice";

const FileComplaint = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(setActivePage(3));
  }, [dispatch]);

  return (
    <div id="file-complaints">
      <ComplaintForm />
    </div>
  );
};

export default FileComplaint;
