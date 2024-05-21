document.addEventListener("DOMContentLoaded", function () {
  const submitButtons = document.querySelectorAll('.image-container form input[type="submit"]');
  const imageContainers = document.querySelectorAll('.image-container');
  const counter = document.getElementById('counter');

  // Initialize state on page load
  imageContainers.forEach((container) => {
    const image = container.querySelector(".image");
    const guessId = image.id;

    // Check if the image has already been answered correctly
    if (localStorage.getItem(`answered-${guessId}`)) {
      image.classList.add("correct");
    }
  });

  submitButtons.forEach((submitButton) => {
    submitButton.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default form submission

      const container = event.target.closest(".image-container");
      if (!container) {
        console.error('No container found for the submit button.');
        return;
      }

      const image = container.querySelector(".image");
      if (!image) {
        console.error('No image found in the container.');
        return;
      }

      const guessId = image.id;
      const userInput = container.querySelector(".user-input").value;

      // Send request to /check_answer endpoint
      fetch(`/check_answer/${guessId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_guess: userInput,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.isCorrect) {
            image.classList.add("correct");
            localStorage.setItem(`answered-${guessId}`, true);
          } else {
            console.error("Incorrect answer:", data.message);
          }
        })
        .catch((error) => {
          console.error("Error checking answer:", error);
        });

      // Send request to / endpoint
      fetch('/', {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          [`text-input-${guessId}`]: userInput
        })
      })
        .then((response) => response.json()) // Handle response as JSON
        .then((data) => {
          // Process the JSON response
          console.log("Response from index:", data);
          // Update the counter in the HTML
          counter.textContent = `You have guessed ${data.correct_answers}/${data.total_items} correctly`;
        })
        .catch((error) => {
          console.error("Error sending data to index:", error);
        });
    });
  });

  document.getElementById('reset-game').addEventListener('click', function () {
    localStorage.clear();
    document.querySelectorAll('.image').forEach((image) => {
      image.classList.remove('correct');
    });
    console.log('Game reset, localStorage cleared.');
  });
});
