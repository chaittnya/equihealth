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

const ChartBedCount = () => {
  const { districts, hospitals, loaded } = useSelector((state) => state.healthInfra);

  if (!loaded) {
    return <p>Loading chart...</p>;
  }

  if (!districts?.allIds?.length) {
    return <p>No data available for this chart.</p>;
  }

  const data = (districts.allIds || []).map((districtId) => {
    const district = districts.byId[districtId];
    const totalBeds = (district.hospitals || [])
      .map((hid) => hospitals.byId[hid]?.total_beds || 0)
      .reduce((a, b) => a + b, 0);
    return { name: district.district_name, beds: totalBeds };
  });

  return (
    <div className="chart">
      <h2 className="chart-title">Total Beds per District</h2>

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
          <Bar dataKey="beds" fill="#00897B" radius={[5, 5, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="chart-insights">
        <p>
          <strong>Key Insights:</strong>
        </p>
        <ul>
          <li className="paper">
            Pune, Mumbai, Thane, and Nashik have the highest number of total
            beds, showing strong healthcare capacity.
          </li>
          <li className="paper">
            Palghar, Gadchiroli, Hingoli, and Nandurbar have very low bed
            availability, indicating weaker health infrastructure.
          </li>
          <li className="paper">
            Rural and tribal districts consistently appear on the lower end of
            bed capacity.
          </li>
          <li className="paper">
            There is a large gap between high-capacity districts like Pune and
            low-capacity ones like Palghar, highlighting inequality.
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ChartBedCount;
