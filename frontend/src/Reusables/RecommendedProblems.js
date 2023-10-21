import { useEffect, useState } from "react";
import { ReactComponent as Reload } from "../Misc/reload.svg";
import Load from "./Load";

function RecommendedProblems({ handle }) {
  const [loading, setLoading] = useState(false);
  const [problems, setProblems] = useState([]);

  const getLink = (id) => {
    const baseLink = "https://codeforces.com/problemset/problem/";
    if (id[id.length - 1] >= "0" && id[id.length - 1] <= "9") {
      return (
        baseLink +
        `${id.substr(0, id.length - 3)}/${id.substr(
          id.length - 2,
          id.length - 1
        )}`
      );
    }

    return baseLink + `${id.substr(0, id.length - 2)}/${id[id.length - 1]}`;
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await fetch(`/recommend/${handle}?limit=5`);
      const jsonData = await data.json();

      console.log(jsonData);
      setProblems(jsonData.recommended_problems);
      setLoading(false);
    };

    fetchData();
  }, [handle]);

  return (
    <div className="recommended-problems">
      <div className="recommended-top">
        <h1>Recommended problems</h1>
        <Reload />
      </div>
      {loading ? (
        <Load />
      ) : (
        <>
          {problems.map((problem) => {
            return (
              <div key={problem.id} className="recommended-kid">
                <p>
                  <a href={getLink(problem.id)}>{problem.name}</a>
                </p>
                <p>{problem.rating}</p>
              </div>
            );
          })}
        </>
      )}
    </div>
  );
}

export default RecommendedProblems;
