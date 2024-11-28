import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SponsorLeaderboard = ({ sponsor }) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log(`Fetching leaderboard data for sponsor: ${sponsor}`);
        const response = await axios.get(`/api/leaderboard/${sponsor}`);
        console.log(`Response status code: ${response.status}`);
        console.log(`Response data: ${JSON.stringify(response.data)}`);
        
        if (response.status === 200) {
          setLeaderboard(response.data);
          console.log(`Successfully fetched leaderboard data for sponsor: ${sponsor}`);
        } else {
          console.error(`Error fetching leaderboard data: ${response.status} - ${response.statusText}`);
          setError(`Error: ${response.status} - ${response.statusText}`);
        }
      } catch (error) {
        console.error(`Error fetching leaderboard data for sponsor: ${sponsor}`, error);
        setError(`An error occurred: ${error.message}`);
      }
    };
    fetchData();
  }, [sponsor]);

  if (error) {
    console.error(`Error component rendering: ${error}`);
    return (
      <div className="error-message text-red-500">
        {error}
        <div>To assist in troubleshooting, please copy the logs shown in the console and provide them to the development team.</div>
      </div>
    );
  }

  return (
    <div className="leaderboard-page">
      <h2 className="text-3xl font-semibold mb-6 text-center text-white">{sponsor} Leaderboard</h2>
      <div className="flex justify-center gap-8 mb-8">
        {leaderboard.slice(0, 3).map((entry, index) => (
          <div key={index} className={`p-6 rounded-xl shadow-lg bg-gray-800 ${index === 0 ? 'scale-110' : ''}`}>
            <h3 className="text-2xl font-bold text-yellow-500">{index + 1} Place: {entry.username}</h3>
            <p className="text-lg text-gray-300">Wager: ${entry.wagerAmount.toLocaleString()}</p>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        {leaderboard.slice(3).map((entry, index) => (
          <div key={index} className="p-4 rounded-xl shadow-md bg-gray-700">
            <h4 className="text-lg text-white">{index + 4} Place: {entry.username}</h4>
            <p className="text-md text-gray-300">Wager: ${entry.wagerAmount.toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SponsorLeaderboard;
