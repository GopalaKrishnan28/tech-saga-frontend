import React from "react";
import ProfilePage from "./ProfilePage"; 
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";// Import ProfilePage
import BidPage from "./BidPage";
import BidStatusPage from "./BidStatusPage";
import TransactionPage from "./TransactionPage";
import BidUpload from "./BidUpload";
import BidManagementPage from "./BidManagementPage";
import ConfirmDeliveryPage from "./ConfirmDeliveryPage";
function App() {
  return (
    <div>
      
      <Router>
      <Routes>
        <Route path="/" element={<ProfilePage />} />
        <Route path="/bid" element={<BidPage />} />
        <Route path="/bidstatus" element={<BidStatusPage />} />
        <Route path="/transaction" element={<TransactionPage />} />
        <Route path="/bidupload" element={<BidUpload />} />
        <Route path="/bidconfirm" element={<BidManagementPage />} />
        <Route path="/delivery" element={<ConfirmDeliveryPage />} />
      </Routes>
    </Router> {/* Render the ProfilePage component */}
    </div>
  );
}

export default App;
