import React from 'react';

const Leaderboard = ({ leaderboard }) => {
  console.log("Leaderboard component loaded.");

  return (
    <div className="leaderboard">
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

export default Leaderboard;
