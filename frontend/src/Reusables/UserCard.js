import { Doughnut } from "react-chartjs-2";
import RecommendedProblems from "./RecommendedProblems";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Colors } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, Colors);

function UserCard({ user }) {
  const tagChartData = (user) => {
    const solvedProblems = user.solved_problems;
    const tagFrequency = {};
    const colors = [];

    solvedProblems.forEach((problem) => {
      problem.tags.forEach((tag) => {
        if (tag in tagFrequency === false) {
          tagFrequency[tag] = 0;
          const randomColor =
            "#" + Math.floor(Math.random() * 16777215).toString(16);
          colors.push(randomColor);
        }
        ++tagFrequency[tag];
      });
    });

    const chartData = {
      labels: Object.keys(tagFrequency),
      datasets: [
        {
          label: "Number of solved problems",
          data: Object.values(tagFrequency),
        },
      ],
    };

    return chartData;
  };

  const chartData = tagChartData(user);

  return (
    <div className="user-card">
      <h1>{user.handle}</h1>
      <div className="donut-container">
        <div className="donut">
          <h1> Solved problems by tags</h1>
          <Doughnut data={chartData} />
        </div>
      </div>
      <RecommendedProblems handle={user.handle} />
    </div>
  );
}

export default UserCard;
