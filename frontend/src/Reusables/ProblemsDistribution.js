import React, { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import Load from "./Load";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function ProblemsDistribution({ user }) {
  const [data, setData] = useState({ labels: [], datasets: [] });
  const [loading, setLoading] = useState(false);

  const options = {
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  const getUserSolved = () => {
    const solved = {};
    for (let i = 800; i <= 3500; i += 100) {
      solved[i] = 0;
    }

    user.solved_problems.forEach((problem) => {
      ++solved[problem.rating];
    });

    return Object.values(solved);
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);

      const dataFetch = await fetch("/distribution/problems");
      const jsonData = await dataFetch.json();

      const obj = {
        labels: Object.keys(jsonData.distribution),
        datasets: [
          {
            label: "Average",
            data: Object.values(jsonData.distribution),
            backgroundColor: "#e6b17e",
          },
          {
            label: user.handle,
            data: getUserSolved(),
            backgroundColor: "#4d331f",
          },
        ],
      };

      setData(obj);

      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <>
      {loading === false ? (
        <div className="problem-distribution">
          <h1>Problems solved by rating</h1>
          <Bar data={data} options={options} />
        </div>
      ) : (
        <Load />
      )}
    </>
  );
}

export default ProblemsDistribution;
