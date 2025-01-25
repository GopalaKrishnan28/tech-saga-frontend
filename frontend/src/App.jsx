import React from "react";
import ProfilePage from "./ProfilePage"; 
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";// Import ProfilePage
import BidPage from "./BidPage";
function App() {
  return (
    <div>
      
      <Router>
      <Routes>
        <Route path="/" element={<ProfilePage />} />
        <Route path="/bid" element={<BidPage />} />
        
      </Routes>
    </Router> {/* Render the ProfilePage component */}
    </div>
  );
}

export default App;
