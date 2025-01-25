import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TransactionPage = () => {
  const [transactions, setTransactions] = useState([]);
  const sellerId = 1;  // Simulating logged-in seller_id
  const apiUrl = "http://127.0.0.1:5000";  // Base API URL

  // Fetch completed transactions
  const fetchCompletedTransactions = async () => {
    try {
      const response = await axios.get(`${apiUrl}/completed_transactions/${sellerId}`);
      setTransactions(response.data);
    } catch (error) {
      console.error("Error fetching completed transactions:", error);
    }
  };

  useEffect(() => {
    fetchCompletedTransactions();
  }, []);

  const downloadInvoice = (transactionId) => {
    window.location.href = `${apiUrl}/download_invoice/${transactionId}`;
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Transaction Page</h1>

      {/* Transaction Section */}
      <div className="mt-8">
        <h2 className="text-xl font-bold">Completed Transactions</h2>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {transactions.map((transaction) => (
            <div key={transaction.transaction_id} className="border p-4 rounded-md">
              <h3 className="font-semibold">{transaction.product}</h3>
              <p><strong>Price:</strong> {transaction.price}</p>
              <p><strong>Quantity:</strong> {transaction.quantity}</p>
              <p><strong>Properties:</strong> {transaction.properties}</p>
              <p><strong>Buyer ID:</strong> {transaction.buyer_id}</p>
              <p><strong>Seller ID:</strong> {transaction.seller_id}</p>
              <button
                onClick={() => downloadInvoice(transaction.transaction_id)}
                className="bg-blue-500 text-white px-4 py-2 rounded-md mt-4"
              >
                Download Invoice
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TransactionPage;
