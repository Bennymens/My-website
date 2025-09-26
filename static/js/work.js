// Project filtering functionality for work.html
document.addEventListener("DOMContentLoaded", function () {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");

  filterButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Remove active class from all buttons
      filterButtons.forEach((btn) => btn.classList.remove("active"));

      // Add active class to clicked button
      this.classList.add("active");

      const filterValue = this.getAttribute("data-filter");

      // Filter project cards
      projectCards.forEach((card) => {
        if (filterValue === "all") {
          card.style.display = "block";
        } else {
          const category = card.getAttribute("data-category");
          if (category === filterValue) {
            card.style.display = "block";
          } else {
            card.style.display = "none";
          }
        }
      });
    });
  });
});

// Animate skill level bars when they come into view
const observerOptions = {
  threshold: 0.2,
  rootMargin: "0px 0px -50px 0px",
};

const skillsObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const levelBars = entry.target.querySelectorAll(".level-bar");
      levelBars.forEach((bar) => {
        bar.style.width = bar.style.width || "0%";
      });
    }
  });
}, observerOptions);

// Observe tech categories
document.querySelectorAll(".tech-category").forEach((category) => {
  skillsObserver.observe(category);
});
