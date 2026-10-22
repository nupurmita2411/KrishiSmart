import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [listening, setListening] = useState(false);
  const navigate = useNavigate();

  const handleMic = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      alert("Ei browser-e voice support nai. Chrome use koro.");
      return;
    }
    const rec = new SR();
    rec.lang = "bn-BD";
    rec.onstart = () => setListening(true);
    rec.onend = () => setListening(false);
    rec.onresult = (e) => setName(e.results[0][0].transcript);
    rec.start();
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/home");
  };

  return (
    <div className="login-wrap">
      <div className="login-hero">
        <div className="login-hero-icon">
  <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
    <path
      d="M20 4C11 4 5 9 5 16c0 1.2.2 2.2.5 3C7 14 11 11 15 10c-3 2-6 5-7.6 9.5C9 20.5 11 21 13 21c7 0 8-9 7-17z"
      fill="#ffffff"
    />
    <path
      d="M5.5 19C7 14 11 11 15 10"
      stroke="#14532d"
      strokeWidth="1.2"
      strokeLinecap="round"
    />
  </svg>
</div>
        <h1>KrishiSmart</h1>
        <p>Protecting crops, securing livelihoods, powered by AI.</p>
      </div>

      <div className="login-side">
        <form className="login-card" onSubmit={handleSubmit}>
          <h2>Welcome Back</h2>
          <p className="login-sub">Sign in to your KrishiSmart account.</p>

          <label>UserName</label>
          <input
            type="text"
            placeholder="আপনার নাম লিখুন"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <label>
            Mobile Number <span className="optional">(optional)</span>
          </label>
          <input
            type="tel"
            placeholder="017XXXXXXXX"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />

          <button
            type="button"
            className={`mic-btn ${listening ? "listening" : ""}`}
            onClick={handleMic}
          >
            🎤 {listening ? "Listening..." : "Press Mic to Speak Your Name"}
          </button>

          <button type="submit" className="btn login-btn">
            EASY ENTER / SIGN IN
          </button>

          <p className="login-note">
            *No password or mobile number required for quick access.
          </p>
        </form>
      </div>
    </div>
  );
}