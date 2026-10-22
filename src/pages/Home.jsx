import { Link } from "react-router-dom";

const icon = (children) => (
  <svg
    width="34"
    height="34"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {children}
  </svg>
);

const cards = [
  {
    to: "/detector",
    title: "Crop Disease Detector",
    text: "Upload leaf photo for instant AI diagnosis.",
    color: "green",
    icon: icon(
      <>
        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
        <circle cx="12" cy="13" r="4" />
      </>
    ),
  },
  {
    to: "/prices",
    title: "Daily Market Rates",
    text: "Real-time wholesale & retail prices.",
    color: "orange",
    icon: icon(
      <>
        <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
        <polyline points="16 7 22 7 22 13" />
      </>
    ),
  },
  {
    to: "/weather",
    title: "Weather Advisory",
    text: "Localized rainfall & irrigation alerts.",
    color: "blue",
    icon: icon(<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />),
  },
  {
    to: "/helpline",
    title: "Krishi Helpline",
    text: "Direct contact with agri officers.",
    color: "purple",
    icon: icon(
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" />
    ),
  },
];

export default function Home() {
  return (
    <div className="page">
      <div className="home-banner">
        <h1>Welcome to KrishiSmart</h1>
        <p>Protect your crops and get fair prices with AI assistance.</p>
      </div>

      <div className="home-grid">
        {cards.map((c) => (
          <Link to={c.to} key={c.to} className={`home-card ${c.color}`}>
            <div className="home-icon">{c.icon}</div>
            <h3>{c.title}</h3>
            <p>{c.text}</p>
            <span className="home-arrow">Open →</span>
          </Link>
        ))}
      </div>
    </div>
  );
}