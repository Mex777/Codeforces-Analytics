import { useState } from "react";

function SearchBar() {
  const [inputValue, setInputValue] = useState("");
  const submit = (e) => {
    e.preventDefault();
    window.location.href = `/user/${inputValue}`;

    console.log(inputValue);
  };

  return (
    <div className="search-bar">
      <form onSubmit={submit}>
        <h2>Unlock Your Full Coding Potential with AICAP</h2>
        <input
          type="search"
          placeholder="Introduce your Codeforces handle"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        ></input>
      </form>
    </div>
  );
}

export default SearchBar;
