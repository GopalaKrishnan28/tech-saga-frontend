import React, { useState, useEffect } from "react";
import axios from "axios";

const ConfirmDeliveryPage = () => {
  const [pendingDeliveries, setPendingDeliveries] = useState([]);
  const apiUrl = "http://127.0.0.1:5000"; // Base API URL
  const buyerId = 1; // Simulated logged-in buyer ID

  // Fetch pending deliveries
  const fetchPendingDeliveries = async () => {
    try {
      const response = await axios.get(`${apiUrl}/pending_deliveries/${buyerId}`);
      setPendingDeliveries(response.data);
    } catch (error) {
      console.error("Error fetching pending deliveries:", error);
    }
  };

  // Confirm delivery
  const confirmDelivery = async (bidId) => {
    try {
      const response = await axios.post(`${apiUrl}/confirm_delivery/${buyerId}/${bidId}`);
      if (response.status === 200) {
        alert("Delivery confirmed successfully");
        fetchPendingDeliveries(); // Refresh pending deliveries
      } else {
        alert("Failed to confirm delivery");
      }
    } catch (error) {
      console.error("Error confirming delivery:", error);
    }
  };

  useEffect(() => {
    fetchPendingDeliveries();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Confirm Delivery</h1>
      <div className="mt-8">
        <h2 className="text-xl font-bold">Pending Deliveries</h2>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {pendingDeliveries.map((delivery) => (
            <div key={delivery.bid_id} className="border p-4 rounded-md">
              <h3 className="font-semibold">Product: {delivery.product}</h3>
              <p><strong>Quantity:</strong> {delivery.quantity}</p>
              <p><strong>Price:</strong> {delivery.price}</p>
              <p><strong>Properties:</strong> {delivery.properties}</p>
              <p><strong>Seller ID:</strong> {delivery.seller_id}</p>
              <button
                onClick={() => confirmDelivery(delivery.bid_id)}
                className="bg-green-500 text-white px-4 py-2 rounded-md mt-4"
              >
                Confirm Delivery
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ConfirmDeliveryPage;
