const API_BASE = "http://localhost:8000";

async function apiGet(path) {
  const res = await fetch(API_BASE + path, {
    headers: authHeader()
  });
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(API_BASE + path, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(body)
  });
  return res.json();
}
