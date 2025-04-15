function getCookie(name) {
  // Getting the Csrf toekn value
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      // Check if this cookie string begins with the name we want
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// below is ajax code for liking a post and updating the like count
document.querySelectorAll("button[id^='likeButton_']").forEach((button) => {
  button.addEventListener("click", function (e) {
    e.preventDefault();
    const postId = this.id.split("_")[1]; // Extract the unique post ID
    const csrftoken = getCookie("csrftoken"); // using the Csrf token value here

    // Create form data with the relevant post id and user id
    const formData = new FormData();
    formData.append("Post", postId);

    // Append CSRF token (make sure the token is rendered correctly)
    formData.append("csrfmiddlewaretoken", csrftoken);
    // Perform Ajax request using Fetch API
    fetch("http://127.0.0.1:8000/like/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the like count
        document.getElementById(`likeCount_${postId}`).textContent =
          data.like_count + " likes";
        // Update the icon based on whether the post is liked
        const likeIcon = document.getElementById(`likeIcon_${postId}`);
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
});

// Below is another ajax code for commenting on a post and updating the comment count

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".comment-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const postId = form.querySelector('input[name="Post"]').value;
      const userId = form.querySelector('input[name="User"]').value;
      const commentText = form.querySelector('input[name="comment"]').value;
      const csrfToken = form.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      fetch("http://127.0.0.1:8000/addcomment/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Post: postId,
          User: userId,
          comment: commentText,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Update the comment count
            const commentCountSpan = document.getElementById(
              `comment-count-${postId}`
            );
            commentCountSpan.textContent = data.comment_count;

            //  Append new comment to the comment section
            // const commentSection = document.getElementById(
            //   `comment-section-${postId}`
            // );
            // const newComment = document.createElement("p");
            // newComment.textContent = data.comment_text;
            // commentSection.appendChild(newComment);
            form.reset();
          } else {
            alert("Error adding comment.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
});
