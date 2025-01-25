import React, { useState } from 'react';
import axios from 'axios';

const BidUpload = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [bidDetails, setBidDetails] = useState({
    product: '',
    quantity: '',
    deadline: '',
    properties: '',
  });

  const buyerId = 1; // Simulating a logged-in buyer_id

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBidDetails({ ...bidDetails, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/upload_bid', {
        ...bidDetails,
        buyer_id: buyerId,
      });
      alert(response.data.message);
      setIsDialogOpen(false);
      setBidDetails({
        product: '',
        quantity: '',
        deadline: '',
        properties: '',
      });
    } catch (error) {
      console.error('Error uploading bid:', error);
      alert('Failed to upload bid.');
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Bid Upload</h1>
      <button
        onClick={() => setIsDialogOpen(true)}
        className="bg-blue-500 text-white px-4 py-2 rounded-md"
      >
        +
      </button>

      {isDialogOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-md w-1/3">
            <h2 className="text-xl font-bold mb-4">Add New Bid</h2>
            <input
              type="text"
              name="product"
              placeholder="Product Name"
              value={bidDetails.product}
              onChange={handleInputChange}
              className="w-full border rounded p-2 mb-4"
            />
            <input
              type="number"
              name="quantity"
              placeholder="Quantity"
              value={bidDetails.quantity}
              onChange={handleInputChange}
              className="w-full border rounded p-2 mb-4"
            />
            <input
              type="date"
              name="deadline"
              placeholder="Deadline"
              value={bidDetails.deadline}
              onChange={handleInputChange}
              className="w-full border rounded p-2 mb-4"
            />
            <textarea
              name="properties"
              placeholder="Properties"
              value={bidDetails.properties}
              onChange={handleInputChange}
              className="w-full border rounded p-2 mb-4"
            />
            <button
              onClick={handleSubmit}
              className="bg-green-500 text-white px-4 py-2 rounded-md mr-2"
            >
              Submit
            </button>
            <button
              onClick={() => setIsDialogOpen(false)}
              className="bg-red-500 text-white px-4 py-2 rounded-md"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BidUpload;
