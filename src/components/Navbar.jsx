import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h2 className="logo">
  <svg
    width="26"
    height="26"
    viewBox="0 0 24 24"
    fill="none"
    style={{ verticalAlign: "middle", marginRight: "8px" }}
  >
    <path
      d="M20 4C11 4 5 9 5 16c0 1.2.2 2.2.5 3C7 14 11 11 15 10c-3 2-6 5-7.6 9.5C9 20.5 11 21 13 21c7 0 8-9 7-17z"
      fill="#ffffff"
    />
  </svg>
  KrishiSmart
</h2>
      <div className="links">
        <NavLink to="/home">Home</NavLink>
        <NavLink to="/detector">Disease Detector</NavLink>
        <NavLink to="/prices">Market Prices</NavLink>
        <NavLink to="/weather">Weather</NavLink>
        <NavLink to="/helpline">Helpline</NavLink>
      </div>
    </nav>
  );
}