import { redirect } from "react-router-dom";
import "./App.css";
import { useState } from "react";
import Header from "./Reusables/Header";
import SearchBar from "./Reusables/SearchBar";
import Banner from "./Reusables/Banner";
import UserReviews from "./Reusables/UserReviews";

function Home() {
  return (
    <>
      <Header />
      <SearchBar />
      <Banner content="Why?" />
      <div className="why">
        <p>
          At AICAP, we transform your Codeforces experience into a data-driven,
          personalized learning adventure. Here's what sets us apart:
        </p>

        <div>
          <p>
            <b>1. Deep Activity Insights:</b>
            <br /> Unlock a comprehensive view of your Codeforces journey.
            Visualize your solved problems, track your progress over time, and
            identify areas for improvement through intuitive charts and
            analytics.
          </p>

          <p>
            <b>2. Smart Recommendations:</b>
            <br /> Never waste a moment wondering what to solve next. AICAP's
            Recommender System analyzes your strengths and weaknesses,
            suggesting tailored problems to enhance your skills efficiently.
          </p>

          <p>
            <b>3. Rating Precision: </b>
            <br /> Dreaming of a specific Codeforces rating? Our Rating
            Predictor uses your contest history to estimate the time needed to
            reach your desired rating, guiding your efforts effectively.
          </p>
        </div>
      </div>

      <Banner content="User Reviews" />
      <UserReviews />
    </>
  );
}

export default Home;
