"use client";
import React, { PureComponent, useEffect, useState } from "react";
import {
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const initialData = [
  { name: "Page A", uv: 4000 },
  { name: "Page B", uv: 3000 },
  { name: "Page C", uv: 2000 },
  { name: "Page D", uv: 2780 },
  { name: "Page E", uv: 1890 },
  { name: "Page F", uv: 2390 },
  { name: "Page G", uv: 3490 },
];

const LinearRegressionChart = () => {
  const [data, setData] = useState(initialData);
  const [iterations, setIterations] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      if (iterations < 50) {
        // Number of training iterations
        trainModel();
        setIterations(iterations + 1);
      } else {
        clearInterval(interval);
      }
    }, 500); // Interval between iterations in milliseconds

    return () => clearInterval(interval);
  }, [iterations]);

  const trainModel = () => {
    const learningRate = 0.1; // Adjust as needed
    const newData = data.map((entry) => ({
      name: entry.name,
      uv: entry.uv - learningRate * Math.random() * 500, // Simulate gradient descent
    }));
    setData(newData);
  };
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart
        width={500}
        height={400}
        margin={{
          top: 10,
          right: 30,
          left: 0,
          bottom: 0,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Scatter name="Training Data" data={data} fill="#8884d8" />
      </ScatterChart>
    </ResponsiveContainer>
  );
};

export default LinearRegressionChart;
