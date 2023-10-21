import { useEffect, useState } from "react";

import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import Load from "./Load";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
);

// const options = {
//   responsive: true,
//   plugins: {
//     legend: {
//       position: 'top' as const,
//     },
//     title: {
//       display: true,
//       text: 'Chart.js Line Chart',
//     },
//   },
// };

function RatingDistribution({ rating }) {
  const [data, setData] = useState({ labels: [], datasets: [] });
  const [loading, setLoading] = useState(false);

  const computeTop = (rating) => {
    rating = Number(rating);
    rating -= rating % 100;
    rating /= 100;

    if (data.datasets.length === 0) {
      return;
    }

    let total = 0;
    for (let i = 0; i <= rating; ++i) {
      total += parseFloat(data.datasets[0].data[i]);
    }

    return Math.round(100 - total);
  };

  const options = {
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const dataS = await fetch("/distribution/rating");
      const jsonData = await dataS.json();

      const labels = Object.keys(jsonData.distribution);
      labels.pop();

      const dataArr = Object.values(jsonData.distribution);
      dataArr.pop();

      const obj = {
        labels,
        datasets: [
          {
            fill: true,
            label: "Percentage",
            data: dataArr,
            borderColor: "#4d331f",
            backgroundColor: "#e6b17e50",
          },
        ],
      };

      setData(obj);
      console.log(data);

      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <>
      {loading === false ? (
        <div className="rating-distribution">
          <h1>Codeforces Rating Distribution</h1>
          {rating !== undefined ? (
            <h2>
              You are in the top {computeTop(rating)}% of players on codeforces
            </h2>
          ) : (
            <></>
          )}
          <Line data={data} options={options} />
        </div>
      ) : (
        <Load />
      )}{" "}
    </>
  );
}

export default RatingDistribution;
