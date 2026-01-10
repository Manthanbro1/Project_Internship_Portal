async function loadCompanyApplications() {
  const res = await fetch(`${API}/company/applications`, {
    headers: getAuthHeaders()
  });

  const apps = await res.json();
  const div = document.getElementById("apps");
  div.innerHTML = "";

  apps.forEach(a => {
    div.innerHTML += `
      <div>
        <p>Status: ${a.status}</p>
        <button onclick="updateStatus(${a.id}, 'Shortlisted')">Shortlist</button>
        <button onclick="reject(${a.id})">Reject</button>
        <hr/>
      </div>
    `;
  });
}

async function updateStatus(id, status) {
  await fetch(`${API}/applications/${id}/status?status=${status}`, {
    method: "PUT",
    headers: getAuthHeaders()
  });
  loadCompanyApplications();
}

async function reject(id) {
  const reason = prompt("Reason for rejection:");
  if (!reason) return;

  await fetch(
    `${API}/applications/${id}/status?status=Rejected&rejection_reason=${reason}`,
    {
      method: "PUT",
      headers: getAuthHeaders()
    }
  );
  loadCompanyApplications();
}

loadCompanyApplications();
