import React from "react";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer id="footer">
      <p>&copy; {year} EquiHealth. All rights reserved.</p>
    </footer>
  );
};

export default Footer;
