import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Load from "./Reusables/Load";
import Header from "./Reusables/Header";
import SearchBar from "./Reusables/SearchBar";
import React from "react";
import UserCard from "./Reusables/UserCard";
import NotFoundPicture from "./Misc/sad-face.png";

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
  }, [handle]);

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
          <div className="container">
            <div className="user-card">
              <h1>The user you searched for does not exist</h1>
              <img src={NotFoundPicture} alt="User not found"></img>
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default UserPage;
