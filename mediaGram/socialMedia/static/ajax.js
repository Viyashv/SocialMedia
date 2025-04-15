document.getElementById("likeButton").addEventListener("click", function (e) {
  e.preventDefault();

  // Create form data
  const formData = new FormData();
  formData.append("Post", "{{ i.id }}"); // Assuming you're in a Django template loop
  formData.append("User", "{{ request.user.id }}"); // Assuming you're in a Django template loop
  // CSRF token
  formData.append("csrfmiddlewaretoken", "{% csrf_token %}");

  // Perform Ajax request using Fetch API
  fetch("http://127.0.0.1:8000/like/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Update the like count
      document.getElementById("likeCount").textContent = data.like_count;
      // Update the icon based on whether the post is liked
      const likeIcon = document.getElementById("likeIcon");
      if (data.liked) {
        likeIcon.classList.remove("bi-heart");
        likeIcon.classList.add("bi-heart-fill");
      } else {
        likeIcon.classList.remove("bi-heart-fill");
        likeIcon.classList.add("bi-heart");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
