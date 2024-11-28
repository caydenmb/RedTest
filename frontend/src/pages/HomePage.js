import React from 'react';
import SponsorButtons from '../components/SponsorButtons';

const HomePage = () => {
  console.log("HomePage component loaded.");

  return (
    <div className="home-page">
      <SponsorButtons />
    </div>
  );
};

export default HomePage;
