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

function getHeaders(includeJson = false) {
  const headers = {
    Authorization: `Bearer ${token}`,
  };

  if (includeJson) {
    headers["Content-Type"] = "application/json";
  }

  return headers;
}

async function safeJson(response) {
  const text = await response.text();
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function loadCompanyProfile() {
  const sector = document.getElementById("sector");
  if (!sector) {
    return;
  }

  const response = await fetch(`${API_BASE}/company/profile`, {
    headers: getHeaders(),
  });
  const profile = await safeJson(response);

  if (!response.ok || !profile) {
    alert("Failed to load company profile");
    return;
  }

  document.getElementById("sector").value = profile.sector || "";
  document.getElementById("description").value = profile.description || "";
  document.getElementById("website").value = profile.website_link || "";
  document.getElementById("linkedin").value = profile.linkedin_link || "";
}

async function saveCompanyProfile() {
  const payload = {
    sector: document.getElementById("sector").value.trim(),
    description: document.getElementById("description").value.trim() || null,
    website_link: document.getElementById("website").value.trim() || null,
    linkedin_link: document.getElementById("linkedin").value.trim() || null,
  };

  const response = await fetch(`${API_BASE}/company/profile`, {
    method: "PUT",
    headers: getHeaders(true),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    alert("Failed to save company profile");
    return;
  }

  alert("Company profile saved");
}

window.saveCompanyProfile = saveCompanyProfile;

const internshipForm = document.getElementById("internshipForm");

if (internshipForm) {
  internshipForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const paidValue = document.getElementById("paid").value === "true";
    const payload = {
      role_title: document.getElementById("role_title").value,
      role_description: document.getElementById("role_description").value,
      required_skills: document.getElementById("required_skills").value,
      paid: paidValue,
      stipend_amount: paidValue
        ? Number(document.getElementById("stipend_amount").value || 0)
        : null,
      mode: document.getElementById("mode").value,
    };

    const response = await fetch(`${API_BASE}/company/internships`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await safeJson(response);
      document.getElementById("error").innerText =
        error?.detail || "Failed to post internship";
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
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      if (!Array.isArray(data)) {
        return;
      }

      data.forEach((internship) => {
        const option = document.createElement("option");
        option.value = internship.id;
        option.textContent = internship.role_title;
        internshipSelect.appendChild(option);
      });
    });
}

if (internshipSelect && projectBox) {
  internshipSelect.addEventListener("change", () => {
    const internshipId = internshipSelect.value;
    projectBox.innerHTML = "";

    if (!internshipId) {
      return;
    }

    fetch(`${API_BASE}/student/projects/recommended/${internshipId}`, {
      headers: getHeaders(),
    })
      .then((res) => res.json())
      .then((data) => {
        if (!Array.isArray(data) || data.length === 0) {
          projectBox.innerHTML = "<p>No matching projects found.</p>";
          return;
        }

        data.forEach((project) => {
          const div = document.createElement("div");
          div.className = "recommend-card";
          div.innerHTML = `
            <h4>${project.title}</h4>
            <p class="recommend-score">Match Score: ${project.similarity_score}%</p>
            <p>Project ID: ${project.project_id}</p>
          `;
          projectBox.appendChild(div);
        });
      });
  });
}

const appBox = document.getElementById("applications");

if (appBox) {
  fetch(`${API_BASE}/company/applications`, {
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      appBox.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        appBox.innerHTML = "<p>No applications yet.</p>";
        return;
      }

      data.forEach((application) => renderApplication(application));
    });
}

function updateStatus(applicationId, status, reason = null) {
  fetch(`${API_BASE}/applications/${applicationId}/status`, {
    method: "PUT",
    headers: getHeaders(true),
    body: JSON.stringify({
      status,
      rejection_reason: reason,
    }),
  }).then(async (response) => {
    if (!response.ok) {
      const error = await safeJson(response);
      alert(error?.detail || "Failed to update status");
      return;
    }

    alert("Status updated");
    window.location.reload();
  });
}

function renderApplication(application) {
  const div = document.createElement("div");
  div.className = "company-app";
  div.innerHTML = `
    <h4>Application #${application.id}</h4>
    <p>Student ID: <strong>${application.student_id}</strong></p>
    <p>Internship ID: <strong>${application.internship_id}</strong></p>
    <p>Status: <strong>${application.status}</strong></p>
    ${
      application.status === "Rejected" && application.rejection_reason
        ? `<p><strong>Reason:</strong> ${application.rejection_reason}</p>`
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

  const [shortlistBtn, selectBtn, rejectBtn] = div.querySelectorAll("button");
  const reasonBox = div.querySelector("textarea");

  shortlistBtn.onclick = () => updateStatus(application.id, "Shortlisted");
  selectBtn.onclick = () => updateStatus(application.id, "Selected");
  rejectBtn.onclick = () => {
    if (!reasonBox.value.trim()) {
      alert("Rejection reason required");
      return;
    }

    updateStatus(application.id, "Rejected", reasonBox.value.trim());
  };

  appBox.appendChild(div);
}

loadCompanyProfile();
