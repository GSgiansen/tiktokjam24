"use client";

import { AreaChart } from "./tremor-raw/area-chart";

const SampleChart = () => {
  const types: Array<"default" | "stacked" | "percent"> = [
    "default",
    "stacked",
    "percent",
  ];

  const chartdata = [
    {
      date: "Jan 23",
      SolarPanels: 2890,
      Inverters: 2338,
    },
    {
      date: "Feb 23",
      SolarPanels: 2756,
      Inverters: 2103,
    },
    {
      date: "Mar 23",
      SolarPanels: 3322,
      Inverters: 2194,
    },
    {
      date: "Apr 23",
      SolarPanels: 3470,
      Inverters: 2108,
    },
    {
      date: "May 23",
      SolarPanels: 3475,
      Inverters: 1812,
    },
    {
      date: "Jun 23",
      SolarPanels: 3129,
      Inverters: 1726,
    },
    {
      date: "Jul 23",
      SolarPanels: 3490,
      Inverters: 1982,
    },
    {
      date: "Aug 23",
      SolarPanels: 2903,
      Inverters: 2012,
    },
    {
      date: "Sep 23",
      SolarPanels: 2643,
      Inverters: 2342,
    },
    {
      date: "Oct 23",
      SolarPanels: 2837,
      Inverters: 2473,
    },
    {
      date: "Nov 23",
      SolarPanels: 2954,
      Inverters: 3848,
    },
    {
      date: "Dec 23",
      SolarPanels: 3239,
      Inverters: 3736,
    },
  ];

  return (
    <div className="flex flex-col gap-16">
      {types.map((type, index) => (
        <div className="flex flex-col gap-4">
          <p className="mx-auto font-mono text-sm font-medium">type="{type}"</p>
          <AreaChart
            key={index}
            type={type}
            className="h-52"
            data={chartdata}
            index="date"
            categories={["SolarPanels", "Inverters"]}
            showLegend={false}
          />
        </div>
      ))}
    </div>
  );
};

export default SampleChart;