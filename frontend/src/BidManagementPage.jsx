import React, { useState, useEffect } from "react";
import axios from "axios";

const BidManagementPage = () => {
  const [bids, setBids] = useState([]);
  const apiUrl = "http://127.0.0.1:5000"; // Base API URL

  // Fetch all bids with bidders
  const fetchBidsWithBidders = async () => {
    try {
      const response = await axios.get(`${apiUrl}/bids_with_bidders`);
      setBids(response.data);
    } catch (error) {
      console.error("Error fetching bids with bidders:", error);
    }
  };

  // Confirm a specific bid
  const confirmBid = async (afterBidId) => {
    try {
      await axios.post(`${apiUrl}/confirm_bidder`, { after_bid_id: afterBidId });
      fetchBidsWithBidders(); // Refresh data after confirmation
    } catch (error) {
      console.error("Error confirming bid:", error);
    }
  };

  useEffect(() => {
    fetchBidsWithBidders();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Manage Bids</h1>

      <div className="mt-8 grid grid-cols-1 gap-8">
        {bids.map((bid) => (
          <div key={bid.bid_id} className="border p-4 rounded-md">
            <h2 className="text-xl font-bold">{bid.product}</h2>
            <p><strong>Quantity:</strong> {bid.quantity}</p>
            <p><strong>Properties:</strong> {bid.properties}</p>
            <p><strong>Deadline:</strong> {bid.deadline}</p>
            <p><strong>Buyer ID:</strong> {bid.buyer_id}</p>

            <h3 className="mt-4 text-lg font-bold">Bidders:</h3>
            {bid.bidders.length === 0 ? (
              <p>No bidders yet.</p>
            ) : (
              <div className="mt-2 space-y-4">
                {bid.bidders.map((bidder) => (
                  <div
                    key={bidder.after_bid_id}
                    className="border p-4 rounded-md"
                  >
                    <p><strong>Bid Price:</strong> {bidder.price}</p>
                    <p><strong>Seller ID:</strong> {bidder.seller_id}</p>
                    <p><strong>Accept:</strong> {bidder.accept}</p>
                    {bidder.accept === "no" && (
                      <button
                        className="bg-blue-500 text-white px-4 py-2 rounded-md mt-4"
                        onClick={() => confirmBid(bidder.after_bid_id)}
                      >
                        Confirm
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BidManagementPage;
