import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BidPage = () => {
  const [currentBids, setCurrentBids] = useState([]);
  const [availableBids, setAvailableBids] = useState([]);
  const [prices, setPrices] = useState({}); // Store prices for each bid
  const sellerId = 1;  // Simulating logged-in seller_id

  const apiUrl = "http://127.0.0.1:5000";  // Base API URL

  // Fetch current bids
  const fetchCurrentBids = async () => {
    try {
      const response = await axios.get(`${apiUrl}/current_bids/${sellerId}`);
      setCurrentBids(response.data);
    } catch (error) {
      console.error("Error fetching current bids:", error);
    }
  };

  // Fetch available bids
  const fetchAvailableBids = async () => {
    try {
      const response = await axios.get(`${apiUrl}/available_bids`);
      setAvailableBids(response.data);
    } catch (error) {
      console.error("Error fetching available bids:", error);
    }
  };

  // Handle price change for a specific bid
  const handlePriceChange = (bidId, newPrice) => {
    setPrices((prevPrices) => ({
      ...prevPrices,
      [bidId]: newPrice,
    }));
  };

  // Confirm bid and move to after_bid table
  const confirmBid = async (bidId) => {
    const price = prices[bidId]; // Get the price for this specific bid
    try {
      await axios.post(`${apiUrl}/confirm_bid`, {
        bid_id: bidId,
        price: price,
        seller_id: sellerId,
      });
      fetchAvailableBids();  // Refresh available bids
      fetchCurrentBids();  // Refresh current bids
    } catch (error) {
      console.error("Error confirming bid:", error);
    }
  };

  useEffect(() => {
    fetchCurrentBids();
    fetchAvailableBids();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Bid Page</h1>

      {/* Current Bids Section */}
      <div className="mt-8">
        <h2 className="text-xl font-bold">Current Bids</h2>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {currentBids.map((bid) => (
            <div key={bid.bid_id} className="border p-4 rounded-md">
              <h3 className="font-semibold">{bid.product}</h3>
              <p>{bid.properties}</p>
              <p><strong>Price:</strong> {bid.price}</p>
              <p><strong>Buyer ID:</strong> {bid.buyer_id}</p> {/* Display buyer_id */}
              {/* Don't show the Confirm button for current bids */}
            </div>
          ))}
        </div>
      </div>

      {/* Available Bids Section */}
      <div className="mt-8">
        <h2 className="text-xl font-bold">Available Bids</h2>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {availableBids.map((bid) => (
            <div key={bid.bid_id} className="border p-4 rounded-md">
              <h3 className="font-semibold">{bid.product}</h3>
              <p>{bid.properties}</p>
              <p><strong>Buyer ID:</strong> {bid.buyer_id}</p> {/* Display buyer_id */}
              <input
                type="number"
                value={prices[bid.bid_id] || ''}
                onChange={(e) => handlePriceChange(bid.bid_id, e.target.value)}
                placeholder="Enter price"
                className="w-full border rounded p-2 mb-4"
              />
              <button
                onClick={() => confirmBid(bid.bid_id)}
                className="bg-blue-500 text-white px-4 py-2 rounded-md"
              >
                Confirm
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BidPage;
