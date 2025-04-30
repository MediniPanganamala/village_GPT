document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const res = await fetch("http://localhost:5000/generate", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    alert('Error generating image');
    return;
  }

  const blob = await res.blob();
  const imageURL = URL.createObjectURL(blob);
  document.getElementById("output-image").src = imageURL;
});
