import React from "react";
import { useSelector } from "react-redux";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const ChartHospitalCount = () => {
  const { loaded } = useSelector((state) => state.healthInfra);
  const districts = useSelector(
    (state) => state.healthInfra?.districts?.byId || {}
  );

  if (!loaded) {
    return <p>Loading chart...</p>;
  }

  if (!districts) {
    return <p>No data available</p>;
  }

  const data = Object.values(districts).map((d) => ({
    name: d.district_name,
    hospitals: d.count,
  }));

  return (
    <div className="chart">
      <h2 className="chart-title">Hospitals per District</h2>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 20, left: 0, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="name"
            angle={-30}
            textAnchor="end"
            interval={0}
            height={80}
          />
          <YAxis />
          <Tooltip />
          <Bar dataKey="hospitals" fill="#26C6DA" radius={[5, 5, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="chart-insights">
        <p>
          <strong>Key Insights:</strong>
        </p>
        <ul>
          <li className="paper">
            Pune, Thane, and Nashik have the highest number of hospitals.
          </li>
          <li className="paper">
            Palghar has the lowest hospital count, indicating weaker coverage.
          </li>
          <li className="paper">
            Rural/tribal districts like Gadchiroli and Hingoli have fewer
            hospitals.
          </li>
          <li className="paper">
            Hospital distribution is uneven across Maharashtra.
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ChartHospitalCount;
