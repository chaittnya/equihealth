import React from "react";
import { useSelector } from "react-redux";
import { useFormik } from "formik";
import Select from "react-select";
import * as Yup from "yup";

import complaintsApi from "../../api/modules/complaintsApi";

const selectStyles = {
  control: (base, state) => ({
    ...base,
    padding: "0.2rem 0",
    border: "none",
    borderBottom: "1px solid black",
    borderRadius: 0,
    boxShadow: "none",
    fontSize: "1.2rem",
    backgroundColor: state.isDisabled ? "#eeeeee" : "#ffffff",
    "&:hover": {
      borderBottom: "1px solid #1E88E5",
    },
  }),
  menu: (base) => ({
    ...base,
    zIndex: 9999,
  }),
  dropdownIndicator: (base, state) => ({
    ...base,
    color: state.isDisabled ? "#bdbdbd" : "#1565C0",
    "&:hover": {
      color: state.isDisabled ? "#bdbdbd" : "#1565C0",
    },
  }),
  clearIndicator: (base, state) => ({
    ...base,
    color: state.isDisabled ? "#bdbdbd" : "#E53935",
    "&:hover": {
      color: state.isDisabled ? "#bdbdbd" : "#E53935",
    },
  }),
};

const ComplaintForm = () => {
  const { districts, hospitals } = useSelector((state) => state.healthInfra);

  const complaintForm = useFormik({
    initialValues: {
      firstName: "",
      lastName: "",
      phoneNumber: "",
      email: "",
      districtId: "",
      hospitalId: "",
      title: "",
      details: "",
    },
    validationSchema: Yup.object({
      firstName: Yup.string()
        .trim()
        .min(2, "First name must be at least 2 characters")
        .max(50, "First name must be at most 50 characters")
        .required("First name is required"),
      lastName: Yup.string()
        .trim()
        .max(50, "Last name must be at most 50 characters"),
      phoneNumber: Yup.string()
        .matches(/^[6-9]\d{9}$/, "Enter a valid 10-digit phone number")
        .required("Phone number is required"),
      email: Yup.string()
        .email("Enter a valid email address")
        .required("Email is required"),
      districtId: Yup.string().required("Please select a district"),
      hospitalId: Yup.string().required("Please select a hospital"),
      title: Yup.string()
        .trim()
        .min(5, "Title must be at least 5 characters")
        .max(200, "Title must be at most 200 characters")
        .required("Title is required"),
      details: Yup.string()
        .trim()
        .min(10, "Details must be at least 10 characters")
        .max(1000, "Details must be at most 1000 characters")
        .required("Please provide more details about your complaint"),
    }),
    onSubmit: async ({
      firstName,
      lastName,
      phoneNumber,
      email,
      stateId,
      districtId,
      hospitalId,
      title,
      details,
    }) => {
      const { res, err } = await complaintsApi.postComplaint({
        firstName,
        lastName,
        phoneNumber,
        email,
        stateId: 18,
        districtId,
        hospitalId,
        title,
        details,
        attachment: null,
      });
      if (res) console.log("success");
      if (err) console.log("failure");
    },
  });

  const districtOptions = districts.allIds.map((id) => {
    const d = districts.byId[id];
    return {
      value: d.district_id,
      label: d.district_name,
    };
  });

  const hospitalOptions = complaintForm.values.districtId
    ? districts.byId[complaintForm.values.districtId].hospitals.map((id) => {
        const h = hospitals.byId[id];
        return {
          value: h.hospital_id,
          label: h.hospital_name,
        };
      })
    : [];

  return (
    <form
      className="complaint-form paper"
      onSubmit={complaintForm.handleSubmit}
    >
      <div className="row">
        <div className="input-field">
          <input
            type="text"
            name="firstName"
            required
            placeholder="First name"
            value={complaintForm.values.firstName}
            onChange={complaintForm.handleChange}
            onBlur={complaintForm.handleBlur}
          />
          <p className="helper-text">
            {complaintForm.touched.firstName && complaintForm.errors.firstName
              ? complaintForm.errors.firstName
              : ""}
          </p>
        </div>
        <div className="input-field">
          <input
            type="text"
            name="lastName"
            required
            placeholder="Last name"
            value={complaintForm.values.lastName}
            onChange={complaintForm.handleChange}
            onBlur={complaintForm.handleBlur}
          />
          <p className="helper-text">
            {complaintForm.touched.lastName && complaintForm.errors.lastName
              ? complaintForm.errors.lastName
              : ""}
          </p>
        </div>
      </div>
      <div className="row">
        <div className="input-field">
          <input
            type="text"
            name="phoneNumber"
            required
            placeholder="Phone number"
            value={complaintForm.values.phoneNumber}
            onChange={complaintForm.handleChange}
            onBlur={complaintForm.handleBlur}
          />
          <p className="helper-text">
            {complaintForm.touched.phoneNumber &&
            complaintForm.errors.phoneNumber
              ? complaintForm.errors.phoneNumber
              : ""}
          </p>
        </div>
        <div className="input-field">
          <input
            type="text"
            name="email"
            required
            placeholder="Email"
            value={complaintForm.values.email}
            onChange={complaintForm.handleChange}
            onBlur={complaintForm.handleBlur}
          />
          <p className="helper-text">
            {complaintForm.touched.email && complaintForm.errors.email
              ? complaintForm.errors.email
              : ""}
          </p>
        </div>
      </div>
      <div className="row">
        <div className="input-field">
          <Select
            className="options"
            styles={selectStyles}
            value={
              districtOptions.find(
                (o) => o.value === complaintForm.values.districtId
              ) || null
            }
            options={districtOptions}
            onChange={(option) => {
              complaintForm.setFieldValue("districtId", option?.value || "");
              complaintForm.setFieldValue("hospitalId", "");
            }}
            onBlur={() => complaintForm.setFieldTouched("districtId", true)}
            placeholder="Select District"
            isClearable
          />
          <p className="helper-text">
            {complaintForm.touched.districtId && complaintForm.errors.districtId
              ? complaintForm.errors.districtId
              : ""}
          </p>
        </div>
        <div className="input-field">
          <Select
            className="options"
            styles={selectStyles}
            value={
              hospitalOptions.find(
                (o) => o.value === complaintForm.values.hospitalId
              ) || null
            }
            options={hospitalOptions}
            onChange={(option) =>
              complaintForm.setFieldValue("hospitalId", option?.value || "")
            }
            onBlur={() => complaintForm.setFieldTouched("hospitalId", true)}
            placeholder="Select Hospital"
            isDisabled={!complaintForm.values.districtId}
            isClearable
          />
          <p className="helper-text">
            {complaintForm.touched.hospitalId && complaintForm.errors.hospitalId
              ? complaintForm.errors.hospitalId
              : ""}
          </p>
        </div>
      </div>
      <div className="row">
        <div className="input-field">
          <input
            type="text"
            name="title"
            required
            placeholder="Title"
            value={complaintForm.values.title}
            onChange={complaintForm.handleChange}
            onBlur={complaintForm.handleBlur}
          />
          <p className="helper-text">
            {complaintForm.touched.title && complaintForm.errors.title
              ? complaintForm.errors.title
              : ""}
          </p>
        </div>
      </div>
      <div className="row">
        <div className="input-field">
          <textarea
            rows={3}
            name="details"
            required
            placeholder="Details"
            value={complaintForm.values.details}
            onChange={complaintForm.handleChange}
            onBlur={complaintForm.handleBlur}
          />
          <p className="helper-text">
            {complaintForm.touched.details && complaintForm.errors.details
              ? complaintForm.errors.details
              : ""}
          </p>
        </div>
      </div>
      <div className="row">
        <button
          type="button"
          className="paper-1"
          onClick={() => complaintForm.resetForm()}
        >
          Clear
        </button>
        <button
          className="paper-1"
          type="submit"
          disabled={!complaintForm.isValid || !complaintForm.dirty}
        >
          Submit
        </button>
      </div>
    </form>
  );
};

export default ComplaintForm;
