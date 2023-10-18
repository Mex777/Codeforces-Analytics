import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import UserPage from "./UserPage";
import NotFound from "./404";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/user/:handle" element={<UserPage />} />
        <Route path="/:invalid" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
