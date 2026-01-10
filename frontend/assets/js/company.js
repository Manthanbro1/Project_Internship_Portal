const API_BASE = "http://localhost:8000";

const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

if (!token || role !== "company") {
  alert("Unauthorized");
  window.location.href = "../../index.html";
}

function logout() {
  localStorage.clear();
  window.location.href = "../../index.html";
}

const internshipForm = document.getElementById("internshipForm");

if (internshipForm) {
  internshipForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const paidValue = document.getElementById("paid").value === "true";

    const payload = {
      role_title: document.getElementById("role_title").value,
      role_description: document.getElementById("role_description").value,
      required_skills: document.getElementById("required_skills").value,
      paid: paidValue,
      stipend_amount: paidValue
        ? Number(document.getElementById("stipend_amount").value || 0)
        : null,
      mode: document.getElementById("mode").value
    };

    const res = await fetch(`${API_BASE}/company/internships`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      document.getElementById("error").innerText =
        "Failed to post internship";
      return;
    }

    alert("Internship posted successfully");
    internshipForm.reset();
  });
}

const internshipSelect = document.getElementById("internshipSelect");
const projectBox = document.getElementById("projects");

if (internshipSelect) {
  fetch(`${API_BASE}/company/internships`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {
    data.forEach(i => {
      const option = document.createElement("option");
      option.value = i.id;
      option.textContent = i.role_title;
      internshipSelect.appendChild(option);
    });
  });
}

if (internshipSelect && projectBox) {
  internshipSelect.addEventListener("change", () => {
    const internshipId = internshipSelect.value;
    projectBox.innerHTML = "";

    if (!internshipId) return;

    fetch(`${API_BASE}/company/projects/recommended/${internshipId}`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.length === 0) {
        projectBox.innerHTML = "<p>No matching projects found.</p>";
        return;
      }

      data.forEach(p => {
        const div = document.createElement("div");
        div.className = "recommend-card";

        div.innerHTML = `
          <h4>${p.title}</h4>
          <p class="recommend-score">
            Match Score: ${p.similarity_score}%
          </p>
          <p>Project ID: ${p.project_id}</p>
        `;

        projectBox.appendChild(div);
      });
    });
  });
}
const appBox = document.getElementById("applications");

if (appBox) {
  fetch(`${API_BASE}/company/applications`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.length === 0) {
      appBox.innerHTML = "<p>No applications yet.</p>";
      return;
    }

    data.forEach(app => renderApplication(app));
  });
}

function updateStatus(application_id, status, reason = null) {
  fetch(`${API_BASE}/applications/${application_id}/status`, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      status: status,
      rejection_reason: reason
    })
  })
  .then(res => {
    if (!res.ok) {
      alert("Failed to update status");
      return;
    }
    alert("Status updated");
    window.location.reload();
  });
}

function renderApplication(app) {
  const div = document.createElement("div");
  div.className = "company-app";

  div.innerHTML = `
    <h4>Application #${app.id}</h4>
    <p>Status: <strong>${app.status}</strong></p>

    ${
      app.status === "Rejected" && app.rejection_reason
        ? `<p><strong>Reason:</strong> ${app.rejection_reason}</p>`
        : ""
    }

    <div class="action-row">
      <button class="btn secondary">Shortlist</button>
      <button class="btn">Select</button>
      <button class="btn secondary">Reject</button>
    </div>

    <textarea
      class="reject"
      placeholder="Rejection reason (required if rejecting)"
    ></textarea>
  `;

  const [shortlistBtn, selectBtn, rejectBtn] =
    div.querySelectorAll("button");

  const reasonBox = div.querySelector("textarea");

  shortlistBtn.onclick = () =>
    updateStatus(app.id, "Shortlisted");

  selectBtn.onclick = () =>
    updateStatus(app.id, "Selected");

  rejectBtn.onclick = () => {
    if (!reasonBox.value.trim()) {
      alert("Rejection reason required");
      return;
    }
    updateStatus(app.id, "Rejected", reasonBox.value);
  };

  appBox.appendChild(div);
}