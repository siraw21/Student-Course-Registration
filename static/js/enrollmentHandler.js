// ── Enrollment Counter (count already-enrolled on page load) ──
const enrolledCounter = document.getElementById("enrolled-counter");
let enrolledCount = document.querySelectorAll(".enroll-btn[disabled]").length;
enrolledCounter.textContent = enrolledCount;

// ── Filter Tabs ───────────────────────────────────────────────
const filterBtns = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".course-card");
const noResults = document.getElementById("no-results");

filterBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    filterBtns.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    const year = btn.dataset.year;
    let visible = 0;

    cards.forEach((card) => {
      const match = year === "all" || card.dataset.year === year;
      card.style.display = match ? "" : "none";
      if (match) visible++;
    });

    noResults.classList.toggle("hidden", visible > 0);
  });
});

// ── Enroll Buttons (your original logic, preserved) ───────────
const enrollBtns = document.querySelectorAll(".enroll-btn");
enrollBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const id = btn.dataset.id;
    enroll(id, btn); // pass btn so we can update it after
  });
});

async function enroll(courseId, btn) {
  const response = await fetch("/enrollment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ course_id: courseId }),
  });

  const data = await response.json();

  if (data.success) {
    alert("Enrolled successfully");
    // Update the button state without a page reload
    btn.textContent = "Enrolled ✓";
    btn.disabled = true;
    enrolledCount++;
    enrolledCounter.textContent = enrolledCount;
  } else {
    alert("Already enrolled");
  }
}
