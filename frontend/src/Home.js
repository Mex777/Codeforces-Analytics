import { redirect } from "react-router-dom";
import "./App.css";
import { useState } from "react";

function Home() {
  const [inputValue, setInputValue] = useState("");

  const submit = (e) => {
    e.preventDefault();
    window.location.href = `/user/${inputValue}`;

    console.log(inputValue);
  };

  return (
    <form onSubmit={submit}>
      <input
        type="search"
        placeholder="Your codeforces handle"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      ></input>
    </form>
  );
}

export default Home;
