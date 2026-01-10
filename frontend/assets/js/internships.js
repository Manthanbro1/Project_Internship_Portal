async function postInternship() {
  const body = {
    role_title: document.getElementById("title").value,
    role_description: document.getElementById("desc").value,
    required_skills: document.getElementById("skills").value,
    paid: document.getElementById("paid").value === "true",
    stipend_amount: Number(document.getElementById("stipend").value) || null,
    mode: document.getElementById("mode").value
  };

  const res = await fetch(`${API}/company/internships`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) alert("Internship posted");
  else alert("Failed to post");
}
