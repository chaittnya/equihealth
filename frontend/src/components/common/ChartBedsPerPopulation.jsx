import React from "react";
import { useSelector } from "react-redux";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const ChartBedsPerPopulation = () => {
  const { districts, hospitals, loaded } = useSelector((state) => state.healthInfra);

  if (!loaded) {
    return <p>Loading chart...</p>;
  }

  if (!districts?.allIds?.length) {
    return <p>No data available for this chart.</p>;
  }

  const data = districts.allIds.map((districtId) => {
    const district = districts.byId[districtId];

    const totalBeds = district.hospitals
      .map((hid) => hospitals.byId[hid]?.total_beds || 0)
      .reduce((a, b) => a + b, 0);

    const population = district.total_persons || 0;

    return {
      name: district.district_name,
      bedsPer10k: population
        ? Number(((totalBeds / population) * 10000).toFixed(2))
        : 0,
    };
  });

  return (
    <div className="chart">
      <h2 className="chart-title">Beds per 10,000 People</h2>

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
          <Bar dataKey="bedsPer10k" fill="#1976D2" radius={[5, 5, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="chart-insights">
        <p>
          <strong>Key Insights:</strong>
        </p>
        <ul>
          <li className="paper">
            Mumbai has the highest beds-per-10k ratio, showing very strong
            medical capacity compared to other districts.
          </li>
          <li className="paper">
            Sindhudurg, Kolhapur, Wardha, and Pune also perform well with
            significantly higher bed availability.
          </li>
          <li className="paper">
            Palghar and Mumbai Suburban have extremely low beds per population
            despite being near major urban regions.
          </li>
          <li className="paper">
            Several districts like Gadchiroli, Hingoli, Buldhana, and Chandrapur
            fall below the ideal threshold, indicating underserved populations.
          </li>
          <li className="paper">
            Large inequalities exist - some districts have over 10 times more
            beds per person than others.
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ChartBedsPerPopulation;
