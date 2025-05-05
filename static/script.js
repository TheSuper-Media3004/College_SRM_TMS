// Wait for DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    // Check for dark mode preference
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Get the theme toggle button
    const themeToggleBtn = document.querySelector('.theme-toggle');

    // Check if dark mode is saved in localStorage
    const savedTheme = localStorage.getItem('darkMode');

    // Apply dark mode if it was previously saved or if user prefers dark mode
    if (savedTheme === 'enabled' || (savedTheme === null && prefersDarkScheme.matches)) {
        document.body.classList.add('dark-mode');
        if (themeToggleBtn) {
            themeToggleBtn.textContent = '☀️ Light Mode';
        }
    } else {
        if (themeToggleBtn) {
            themeToggleBtn.textContent = '🌙 Dark Mode';
        }
    }

    // Add click event to the theme toggle button
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            // Toggle dark-mode class on body
            document.body.classList.toggle('dark-mode');

            // Update button text and save preference to localStorage
            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
                themeToggleBtn.textContent = '☀️ Light Mode';
            } else {
                localStorage.setItem('darkMode', 'disabled');
                themeToggleBtn.textContent = '🌙 Dark Mode';
            }
        });
    }

    // Format time inputs
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Ensure time is displayed in 12-hour format
            const time = this.value;
            if (time) {
                const [hours, minutes] = time.split(':');
                const hour = parseInt(hours, 10);
                const ampm = hour >= 12 ? 'PM' : 'AM';
                const hour12 = hour % 12 || 12;
                this.dataset.displayValue = `${hour12}:${minutes} ${ampm}`;
            }
        });
    });

    // Dynamic boarding points loading
    const routeSelect = document.getElementById('route_id');
    if (routeSelect) {
        routeSelect.addEventListener('change', function() {
            loadBoardingPoints(this.value);
        });
    }

    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseover', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip';
            tooltipEl.textContent = tooltipText;
            document.body.appendChild(tooltipEl);

            const rect = this.getBoundingClientRect();
            tooltipEl.style.top = rect.bottom + 10 + 'px';
            tooltipEl.style.left = rect.left + (rect.width / 2) - (tooltipEl.offsetWidth / 2) + 'px';

            this.addEventListener('mouseout', function() {
                tooltipEl.remove();
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert('Please fill all required fields');
            }
        });
    });

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// Function to load boarding points for a selected route
function loadBoardingPoints(routeId) {
    if (!routeId) return;

    const container = document.getElementById('boarding-points-container');
    const select = document.getElementById('boarding_point_id');

    if (!container || !select) return;

    // Show loading state
    container.style.display = 'block';
    select.innerHTML = '<option value="">Loading boarding points...</option>';

    // Fetch boarding points from server
    fetch(`/get-boarding-points/${routeId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            select.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading boarding points:', error);
            select.innerHTML = '<option value="">Error loading boarding points</option>';
        });
}
