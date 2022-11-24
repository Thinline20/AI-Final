import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

type PlotProps = {};

const Plot = (props: PlotProps) => {
  const options = {
    chart: {
      type: "bar",
    },
    title: {
      text: "Fruit Consumption",
    },
    xAxis: {
      categories: ["Apples", "Bananas", "Oranges"],
    },
    yAxis: {
      title: {
        text: "Fruit Eaten",
      },
    },
    series: [
      {
        name: "Jane",
        data: [1, 0, 4],
      },
      {
        name: "John",
        data: [5, 7, 3],
      },
    ],
  };

  return (
    <>
      <HighchartsReact highcharts={Highcharts} options={options} />
    </>
  );
};

export default Plot;
