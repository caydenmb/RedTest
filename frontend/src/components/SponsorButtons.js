import React from 'react';

const SponsorButtons = () => {
  console.log("SponsorButtons component loaded.");

  const sponsors = [
    { name: "Shuffle.com", link: "https://shuffle.com/?r=Red" },
    { name: "PackDraw.com", link: "https://packdraw.com/?ref=red" }
  ];

  return (
    <div className="flex flex-wrap justify-center gap-6 my-8">
      {sponsors.map((sponsor, index) => (
        <a
          key={index}
          href={sponsor.link}
          className="bg-gradient-to-r from-green-400 to-blue-500 text-white font-bold py-3 px-8 rounded-full transform hover:scale-105 transition-transform"
        >
          {sponsor.name}
        </a>
      ))}
    </div>
  );
};

export default SponsorButtons;
