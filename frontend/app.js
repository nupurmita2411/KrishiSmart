/* Shared helpers used by every page. Owner: Avijit */
function token() { return localStorage.getItem("token"); }
function logout() { localStorage.clear(); location.href = "/index.html"; }

// bi("বাংলা","English") -> Bangla on top, English below
function bi(bn, en) { return `<span class="bn">${bn}</span><span class="en">${en}</span>`; }

async function api(path, options = {}) {
  const headers = options.headers || {};
  if (token()) headers["Authorization"] = "Bearer " + token();
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.body);
  }
  const res = await fetch(path, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (res.status === 401 && token()) logout();   // token expired (server restarted)
    throw new Error(data.detail || "Something went wrong");
  }
  return data;
}

// call at top of a page. requireLogin() or requireLogin(true) for admin pages
function requireLogin(adminOnly = false) {
  if (!token()) { location.href = "/index.html"; return false; }
  if (adminOnly && localStorage.getItem("role") !== "admin") { location.href = "/diagnose.html"; return false; }
  return true;
}

function renderNav() {
  const admin = localStorage.getItem("role") === "admin";
  document.getElementById("nav").innerHTML =
    "<b>🌾 KrishiSmart</b>" +
    (token()
      ? `<a href='/diagnose.html'>${bi("রোগ নির্ণয়", "Diagnose")}</a>
         <a href='/history.html'>${bi("ইতিহাস", "History")}</a>
         <a href='/prices.html'>${bi("বাজারদর", "Prices")}</a>` +
        (admin ? `<a href='/admin.html'>${bi("অ্যাডমিন", "Admin")}</a>` : "") +
        `<a href='#' onclick='logout()'>${bi("লগআউট", "Logout")}</a>`
      : `<a href='/prices.html'>${bi("বাজারদর", "Prices")}</a><a href='/index.html'>${bi("লগইন", "Login")}</a>`);
}
