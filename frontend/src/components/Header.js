import React from 'react';
import { motion } from 'framer-motion';

const Header = () => {
  console.log("Header component loaded.");

  return (
    <header className="text-center my-10">
      <motion.img
        src="/static/redlogo.png"
        alt="Redhunllef Logo"
        className="mx-auto"
        animate={{ y: [0, -15, 0] }}
        transition={{ duration: 1, repeat: Infinity }}
      />
    </header>
  );
};

export default Header;
