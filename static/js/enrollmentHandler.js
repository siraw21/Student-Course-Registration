const enrollBtns = document.querySelectorAll(".enroll-btn");
enrollBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const id = btn.dataset.id;
    enroll(id);
  });
});

async function enroll(courseId) {
  const response = await fetch("/enrollment", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      course_id: courseId,
    }),
  });

  const data = await response.json();
  if (data.success) {
    alert("Enrolled successfully");
  } else {
    alert("Already enrolled");
  }
}
