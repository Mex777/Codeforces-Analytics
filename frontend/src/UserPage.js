import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Load from "./Reusables/Load";
import Header from "./Reusables/Header";
import SearchBar from "./Reusables/SearchBar";
import React from "react";
import UserCard from "./Reusables/UserCard";

function UserPage() {
  const params = useParams();
  const handle = params.handle;
  const [user, setUser] = useState({});
  const [status, setStatus] = useState(200);
  const [useEffectDone, setDone] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetch(`/users/${handle}`);
      console.log(data);

      if (data.status === 404) {
        setStatus(404);
      }

      const jsonData = await data.json();

      if (jsonData.status === "SUCCESS") {
        setUser(jsonData.user);
      }

      setDone(true);
    };

    fetchData();
  }, []);

  return (
    <>
      <Header />
      {useEffectDone === false ? (
        <Load />
      ) : status === 200 ? (
        <>
          <SearchBar />
          <div className="container">
            <UserCard user={user} />
          </div>
        </>
      ) : (
        <>
          <SearchBar />
          <h1>NOT FOUND</h1>
        </>
      )}
    </>
  );
}

export default UserPage;
