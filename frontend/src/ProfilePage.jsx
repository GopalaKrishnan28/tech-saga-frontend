import React, { useState, useEffect } from "react";
import axios from "axios";
import Modal from "react-modal";
import { Link } from "react-router-dom";
Modal.setAppElement("#root");

const ProfilePage = () => {
  const [userId] = useState(1); // Simulate current user_id as 1
  const [profile, setProfile] = useState({});
  const [items, setItems] = useState([]); // Initialize as an empty array
  const [modalOpen, setModalOpen] = useState(false);
  const [newItem, setNewItem] = useState({ productName: "", properties: "" });

  const apiUrl = "http://127.0.0.1:5000"; // Base API URL

  // Fetch seller profile data
  const fetchProfile = async () => {
    try {
      const response = await axios.get(`${apiUrl}/profile/${userId}`);
      console.log(response.name);
      setProfile(response.data);
    } catch (error) {
      console.error("Error fetching profile:", error);
    }
  };

  // Fetch items for the seller
  const fetchItems = async () => {
    try {
      const response = await axios.get(`${apiUrl}/items/${userId}`);
      console.log(response.data); // Log to check the received data
      if (Array.isArray(response.data)) {
        setItems(response.data);
      } else {
        setItems([]); // Handle non-array response
        console.error("Unexpected response format:", response.data);
      }
    } catch (error) {
      console.error("Error fetching items:", error);
      setItems([]); // Handle errors by resetting to an empty array
    }
  };

  // Add a new item
  const addItem = async () => {
    try {
      if (!newItem.productName || !newItem.properties) {
        alert("Please provide both product name and properties.");
        return;
      }

      const itemData = { ...newItem, seller_id: userId };
      const response = await axios.post(`${apiUrl}/add_item/${userId}`, itemData);
      if (response.status === 201) {
        setModalOpen(false); // Close modal after adding
        fetchItems(); // Refresh items
      } else {
        alert("Failed to add item.");
      }
    } catch (error) {
      console.error("Error adding item:", error);
      alert("Error adding item. Please try again.");
    }
  };

  useEffect(() => {
    fetchProfile();
    fetchItems();
  }, [userId]);

  return (
    <div className="p-4">
      {/* Navigation Bar */}
      <nav className="bg-blue-500 text-white p-4 rounded-md flex justify-around">
      <Link to="/profile">Profile</Link>
      <Link to="/bid">Bids</Link>
      <Link to="/transactions">Transaction History</Link>
      <Link to="/bidstatus">bidstatus</Link>
    </nav>

      {/* Profile Section */}
      <div className="mt-8">
        <div className="text-center">
        <img
  src="https://images.pexels.com/photos/1563356/pexels-photo-1563356.jpeg?cs=srgb&dl=pexels-thatguycraig000-1563356.jpg&fm=jpg"
  alt="Profile"
  className="rounded-full"
  style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: '50%' }}
/>

          <h1 className="text-2xl font-semibold mt-4">{profile.name}</h1>
          <p>{profile.address}</p>
          <p>{profile.email}</p>
          <p>{profile.contact_no}</p>
        </div>

        {/* Items Section */}
        <div className="mt-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Items</h2>
            <button
              onClick={() => setModalOpen(true)}
              className="bg-blue-500 text-white px-4 py-2 rounded-md"
            >
              +
            </button>
          </div>
          <ul>
            {items.length > 0 ? (
              items.map((item, index) => (
                <li key={index} className="border p-4 rounded-md mb-2">
                  <strong>{item.productName}</strong>
                  <p>{item.properties}</p>
                </li>
              ))
            ) : (
              <p>No items available.</p>
            )}
          </ul>
        </div>
      </div>

      {/* Add Item Modal */}
      <Modal
        isOpen={modalOpen}
        onRequestClose={() => setModalOpen(false)}
        className="bg-white rounded-lg shadow-lg p-6 mx-auto mt-20 max-w-md"
        overlayClassName="bg-black bg-opacity-50 fixed inset-0"
      >
        <h2 className="text-lg font-bold mb-4">Add Item</h2>
        <div>
          <label className="block mb-2">Product Name</label>
          <input
            type="text"
            value={newItem.productName}
            onChange={(e) =>
              setNewItem({ ...newItem, productName: e.target.value })
            }
            className="w-full border rounded p-2 mb-4"
          />
        </div>
        <div>
          <label className="block mb-2">Properties</label>
          <input
            type="text"
            value={newItem.properties}
            onChange={(e) =>
              setNewItem({ ...newItem, properties: e.target.value })
            }
            className="w-full border rounded p-2 mb-4"
          />
        </div>
        <button
          onClick={addItem}
          className="bg-blue-500 text-white px-4 py-2 rounded-md"
        >
          Add
        </button>
      </Modal>
    </div>
  );
};

export default ProfilePage;
