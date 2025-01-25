import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BidStatusPage = () => {
  const [successfulBids, setSuccessfulBids] = useState([]);
  const [unsuccessfulBids, setUnsuccessfulBids] = useState([]);
  const sellerId = 1;  // Simulating logged-in seller_id
  const apiUrl = "http://127.0.0.1:5000";  // Base API URL

  // Fetch successful bids
  const fetchSuccessfulBids = async () => {
    try {
      const response = await axios.get(`${apiUrl}/successful_bids/${sellerId}`);
      setSuccessfulBids(response.data);
    } catch (error) {
      console.error("Error fetching successful bids:", error);
    }
  };

  // Fetch unsuccessful bids
  const fetchUnsuccessfulBids = async () => {
    try {
      const response = await axios.get(`${apiUrl}/unsuccessful_bids/${sellerId}`);
      setUnsuccessfulBids(response.data);
    } catch (error) {
      console.error("Error fetching unsuccessful bids:", error);
    }
  };

  useEffect(() => {
    fetchSuccessfulBids();
    fetchUnsuccessfulBids();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Bid Status</h1>

      {/* Successful Bids Section */}
      <div className="mt-8">
        <h2 className="text-xl font-bold">Successful Bids</h2>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {successfulBids.map((bid) => (
            <div key={bid.bid_id} className="border p-4 rounded-md">
              <h3 className="font-semibold">{bid.product}</h3>
              <p><strong>Price:</strong> {bid.price}</p>
              <p><strong>Quantity:</strong> {bid.quantity}</p>
              <p><strong>Properties:</strong> {bid.properties}</p>
              <p><strong>Buyer ID:</strong> {bid.buyer_id}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Unsuccessful Bids Section */}
      <div className="mt-8">
        <h2 className="text-xl font-bold">Unsuccessful Bids</h2>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {unsuccessfulBids.map((bid) => (
            <div key={bid.bid_id} className="border p-4 rounded-md">
              <h3 className="font-semibold">{bid.product}</h3>
              <p><strong>Price:</strong> {bid.price}</p>
              <p><strong>Quantity:</strong> {bid.quantity}</p>
              <p><strong>Properties:</strong> {bid.properties}</p>
              <p><strong>Buyer ID:</strong> {bid.buyer_id}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BidStatusPage;
