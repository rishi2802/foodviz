document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior
        const targetClass = this.getAttribute('data-target'); // Get target class
        const targetSection = document.querySelector(targetClass); // Find the section with that class

        // Scroll to the section smoothly
        targetSection.scrollIntoView({
          behavior: 'smooth' // Enable smooth scrolling
        });
      });
    });