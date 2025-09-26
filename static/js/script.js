// Benedict Nii Odartey Mensah - Personal Website JavaScript

// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Initialize all functionality
  initializeProjectCards();
  initializeSmoothScrolling();
  initializeFormHandling();
  initializeNavigationHighlight();
  initializeMobileOptimizations();
  initializeMobileMenu();
  setCurrentYear();

  console.log("Personal website loaded successfully!");
});

// Mobile-specific optimizations
function initializeMobileOptimizations() {
  // Prevent iOS zoom on input focus
  if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
    const viewportMeta = document.querySelector('meta[name="viewport"]');
    if (viewportMeta) {
      viewportMeta.content =
        "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
    }
  }

  // Add touch feedback for interactive elements
  const interactiveElements = document.querySelectorAll(
    ".project, .btn, .skill"
  );

  interactiveElements.forEach((element) => {
    element.addEventListener(
      "touchstart",
      function () {
        this.style.opacity = "0.8";
      },
      { passive: true }
    );

    element.addEventListener(
      "touchend",
      function () {
        this.style.opacity = "1";
      },
      { passive: true }
    );
  });

  // Optimize scroll performance on mobile
  let scrollTimeout;
  let isScrolling = false;

  window.addEventListener(
    "scroll",
    function () {
      if (!isScrolling) {
        requestAnimationFrame(function () {
          // Your scroll handling code here
          isScrolling = false;
        });
        isScrolling = true;
      }
    },
    { passive: true }
  );

  // Handle orientation changes
  window.addEventListener("orientationchange", function () {
    setTimeout(function () {
      // Recalculate layout after orientation change
      window.scrollTo(0, window.pageYOffset);
    }, 100);
  });
}

// Project Cards Functionality
function initializeProjectCards() {
  const projectCards = document.querySelectorAll(".project");

  projectCards.forEach((card) => {
    // Add click/touch handler for project navigation
    card.addEventListener("click", function (e) {
      e.preventDefault();
      const projectUrl = this.dataset.url;

      if (projectUrl && projectUrl !== "#") {
        // Add loading state
        this.classList.add("loading");

        // Provide haptic feedback on supported devices
        if (navigator.vibrate) {
          navigator.vibrate(50);
        }

        // Open project in new tab
        window.open(projectUrl, "_blank", "noopener,noreferrer");

        // Remove loading state after a short delay
        setTimeout(() => {
          this.classList.remove("loading");
        }, 500);
      }
    });

    // Add hover effect for desktop
    card.addEventListener("mouseenter", function () {
      if (!isMobile()) {
        this.style.transform = "translateY(-5px)";
        this.style.boxShadow = "0 8px 25px rgba(0, 0, 0, 0.15)";
      }
    });

    card.addEventListener("mouseleave", function () {
      if (!isMobile()) {
        this.style.transform = "translateY(0)";
        this.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)";
      }
    });
  });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
  const navLinks = document.querySelectorAll('nav a[href^="#"]');

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href").substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        const headerHeight = 80; // Account for fixed header
        const targetPosition =
          targetElement.getBoundingClientRect().top +
          window.pageYOffset -
          headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });

        // Close mobile menu if open
        const mobileMenu = document.querySelector(".nav-links");
        if (mobileMenu && mobileMenu.classList.contains("active")) {
          toggleMobileMenu();
        }
      }
    });
  });
}

// Form Handling
function initializeFormHandling() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const submitButton = this.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;

    // Show loading state
    submitButton.textContent = "Sending...";
    submitButton.disabled = true;
    submitButton.classList.add("loading");

    // Simulate form submission (replace with actual endpoint)
    setTimeout(() => {
      // Show success message
      showFormMessage(
        "Thank you for your message! I'll get back to you soon.",
        "success"
      );

      // Reset form
      this.reset();

      // Reset button
      submitButton.textContent = originalButtonText;
      submitButton.disabled = false;
      submitButton.classList.remove("loading");
    }, 1500);
  });

  // Add real-time validation
  const inputs = form.querySelectorAll("input, textarea");
  inputs.forEach((input) => {
    input.addEventListener("blur", validateField);
    input.addEventListener("input", function () {
      if (this.classList.contains("error")) {
        validateField.call(this);
      }
    });
  });
}

// Field Validation
function validateField() {
  const value = this.value.trim();
  const type = this.type;
  const isRequired = this.required;

  // Remove existing error states
  this.classList.remove("error");
  const existingError = this.parentNode.querySelector(".error-message");
  if (existingError) {
    existingError.remove();
  }

  let isValid = true;
  let errorMessage = "";

  // Required field validation
  if (isRequired && !value) {
    isValid = false;
    errorMessage = "This field is required";
  }
  // Email validation
  else if (type === "email" && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      isValid = false;
      errorMessage = "Please enter a valid email address";
    }
  }
  // Phone validation (basic)
  else if (type === "tel" && value) {
    const phoneRegex = /^[\+]?[0-9\s\-\(\)]+$/;
    if (!phoneRegex.test(value) || value.length < 10) {
      isValid = false;
      errorMessage = "Please enter a valid phone number";
    }
  }

  if (!isValid) {
    this.classList.add("error");
    const errorElement = document.createElement("span");
    errorElement.className = "error-message";
    errorElement.textContent = errorMessage;
    this.parentNode.appendChild(errorElement);
  }

  return isValid;
}

// Show form messages
function showFormMessage(message, type = "info") {
  // Remove existing messages
  const existingMessages = document.querySelectorAll(".form-message");
  existingMessages.forEach((msg) => msg.remove());

  const messageElement = document.createElement("div");
  messageElement.className = `form-message ${type}`;
  messageElement.textContent = message;

  const form = document.getElementById("contact-form");
  form.insertBefore(messageElement, form.firstChild);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (messageElement.parentNode) {
      messageElement.remove();
    }
  }, 5000);
}

// Navigation Highlight
function initializeNavigationHighlight() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll("nav a[href^='#']");

  function highlightNavigation() {
    const scrollPosition = window.pageYOffset + 100;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      const sectionId = section.getAttribute("id");

      if (
        scrollPosition >= sectionTop &&
        scrollPosition < sectionTop + sectionHeight
      ) {
        navLinks.forEach((link) => {
          link.classList.remove("active");
          if (link.getAttribute("href") === `#${sectionId}`) {
            link.classList.add("active");
          }
        });
      }
    });
  }

  window.addEventListener("scroll", highlightNavigation, { passive: true });
  highlightNavigation(); // Run once on load
}

// Mobile Menu Functionality
function initializeMobileMenu() {
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", toggleMobileMenu);

    // Close menu when clicking outside
    document.addEventListener("click", function (e) {
      const isClickInsideNav = navLinks.contains(e.target);
      const isClickOnHamburger = hamburger.contains(e.target);

      if (
        !isClickInsideNav &&
        !isClickOnHamburger &&
        navLinks.classList.contains("active")
      ) {
        toggleMobileMenu();
      }
    });
  }
}

function toggleMobileMenu() {
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.classList.toggle("active");
    navLinks.classList.toggle("active");
    document.body.classList.toggle("menu-open");
  }
}

// Utility Functions
function isMobile() {
  return (
    window.innerWidth <= 768 ||
    /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    )
  );
}

function isTablet() {
  return window.innerWidth > 768 && window.innerWidth <= 1024;
}

function setCurrentYear() {
  const yearElement = document.getElementById("current-year");
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
}

// Intersection Observer for animations
function initializeAnimations() {
  if ("IntersectionObserver" in window) {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-in");
        }
      });
    }, observerOptions);

    // Observe elements that should animate in
    const animatedElements = document.querySelectorAll(
      ".project, .skill, .hero h1, .hero p, .section-title"
    );

    animatedElements.forEach((el) => observer.observe(el));
  }
}

// Performance monitoring
function initializePerformanceMonitoring() {
  // Monitor page load performance
  window.addEventListener("load", function () {
    if ("performance" in window) {
      const loadTime =
        performance.timing.loadEventEnd - performance.timing.navigationStart;
      console.log(`Page loaded in ${loadTime}ms`);

      // Log slow loading times (> 3 seconds)
      if (loadTime > 3000) {
        console.warn("Slow page load detected:", loadTime + "ms");
      }
    }
  });

  // Monitor scroll performance
  let scrollStart = null;
  window.addEventListener(
    "scroll",
    function () {
      if (scrollStart === null) {
        scrollStart = performance.now();
      }
    },
    { passive: true }
  );

  // Error handling
  window.addEventListener("error", function (e) {
    console.error("JavaScript error:", e.error);
  });
}

// Initialize performance monitoring and animations
document.addEventListener("DOMContentLoaded", function () {
  initializeAnimations();
  initializePerformanceMonitoring();
});

// Export functions for testing (if needed)
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    initializeProjectCards,
    initializeSmoothScrolling,
    initializeFormHandling,
    validateField,
    isMobile,
    isTablet,
  };
}
