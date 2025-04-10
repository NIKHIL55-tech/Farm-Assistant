// Farm Assistant Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });

    // Dynamic input fields for farm data
    const addCropBtn = document.getElementById('add-crop-btn');
    if (addCropBtn) {
        addCropBtn.addEventListener('click', function() {
            const cropFields = document.getElementById('crop-fields');
            const cropCount = cropFields.getElementsByClassName('crop-row').length;
            
            const newRow = document.createElement('div');
            newRow.className = 'crop-row row g-3 mb-3';
            newRow.innerHTML = `
                <div class="col-md-4">
                    <input type="text" class="form-control" name="crop_name_${cropCount}" placeholder="Crop Name" required>
                </div>
                <div class="col-md-3">
                    <input type="number" class="form-control" name="crop_area_${cropCount}" placeholder="Area (acres)" required>
                </div>
                <div class="col-md-3">
                    <input type="number" class="form-control" name="crop_yield_${cropCount}" placeholder="Expected Yield" required>
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-danger remove-crop-btn">Remove</button>
                </div>
            `;
            
            cropFields.appendChild(newRow);
            
            // Add event listener to the remove button
            newRow.querySelector('.remove-crop-btn').addEventListener('click', function() {
                cropFields.removeChild(newRow);
            });
        });
    }

    // Handle removal of crop rows
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-crop-btn')) {
            const row = e.target.closest('.crop-row');
            row.parentNode.removeChild(row);
        }
    });

    // Weather data refresh
    const refreshWeatherBtn = document.getElementById('refresh-weather');
    if (refreshWeatherBtn) {
        refreshWeatherBtn.addEventListener('click', function() {
            const weatherContainer = document.getElementById('weather-data');
            weatherContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Fetching latest weather data...</p></div>';
            
            // Simulate fetch delay
            setTimeout(function() {
                fetch('/weather?refresh=true')
                    .then(response => response.text())
                    .then(html => {
                        weatherContainer.innerHTML = html;
                    })
                    .catch(error => {
                        weatherContainer.innerHTML = `<div class="alert alert-danger">Error fetching weather data: ${error}</div>`;
                    });
            }, 1500);
        });
    }

    // Chart animations
    const chartContainers = document.querySelectorAll('.chart-container');
    
    if (chartContainers.length > 0) {
        // Fade in charts when they come into view
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        chartContainers.forEach(container => {
            observer.observe(container);
        });
    }

    // Handle theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            const isDarkTheme = document.body.classList.contains('dark-theme');
            localStorage.setItem('darkTheme', isDarkTheme);
            
            // Update icon
            const icon = themeToggle.querySelector('i');
            if (isDarkTheme) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
        
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('darkTheme');
        if (savedTheme === 'true') {
            document.body.classList.add('dark-theme');
            const icon = themeToggle.querySelector('i');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
}); 