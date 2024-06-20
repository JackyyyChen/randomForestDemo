"use client";

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [linear, setLinear] = useState<string>('');
  const [digital, setDigital] = useState<string>('');
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/predict', {
        Linear: parseFloat(linear),
        Digital: parseFloat(digital),
      });
      setResult(response.data['Predicted Overlap']);
    } catch (error) {
      console.error('Error:', error);
      setError('There was an error processing your request. Please try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="max-w-xl mx-auto p-6 bg-white shadow-md rounded-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Random Forest Regression API</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="form-group">
            <label htmlFor="linear" className="block text-sm font-medium text-gray-700">Linear:</label>
            <input
              type="number"
              id="linear"
              value={linear}
              onChange={(e) => setLinear(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <div className="form-group">
            <label htmlFor="digital" className="block text-sm font-medium text-gray-700">Digital:</label>
            <input
              type="number"
              id="digital"
              value={digital}
              onChange={(e) => setDigital(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <button
            type="submit"
            className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
              loading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'
            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
            disabled={loading}
          >
            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </form>
        {error && <div className="mt-4 text-red-600">{error}</div>}
        {result && <div className="mt-4 text-green-600">Predicted Overlap: {result}</div>}
      </div>
    </div>
  );
}
