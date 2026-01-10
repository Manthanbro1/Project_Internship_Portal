async function loadCompanyProfile() {
  const res = await fetch(`${API}/company/profile`, {
    headers: getAuthHeaders()
  });

  const p = await res.json();
  document.getElementById("sector").value = p.sector || "";
  document.getElementById("description").value = p.description || "";
  document.getElementById("website").value = p.website_link || "";
  document.getElementById("linkedin").value = p.linkedin_link || "";
}

async function saveCompanyProfile() {
  const body = {
    sector: document.getElementById("sector").value,
    description: document.getElementById("description").value,
    website_link: document.getElementById("website").value,
    linkedin_link: document.getElementById("linkedin").value
  };

  const res = await fetch(`${API}/company/profile`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) alert("Profile saved");
  else alert("Failed to save");
}

loadCompanyProfile();
