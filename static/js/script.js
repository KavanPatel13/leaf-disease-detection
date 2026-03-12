document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. Particle System (Spores/Leaves) ---
    const canvas = document.getElementById('bg-particles');
    const ctx = canvas.getContext('2d');
    
    let particles = [];
    const colors = ['#ffaf7b', '#d76d77', '#3a1c71', '#fff3e0', '#ffffff'];
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = canvas.height + Math.random() * 100; // Start below screen
            this.size = Math.random() * 5 + 2;
            this.speedY = Math.random() * 1 + 0.5; // Float up
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.opacity = Math.random() * 0.5 + 0.1;
            this.rotation = Math.random() * 360;
            this.rotationSpeed = (Math.random() - 0.5) * 2;
        }

        update() {
            this.y -= this.speedY;
            this.x += this.speedX;
            this.rotation += this.rotationSpeed;

            // Reset if it goes off top
            if (this.y < -20) {
                this.reset();
            }
        }

        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation * Math.PI / 180);
            ctx.globalAlpha = this.opacity;
            
            // Draw a simple leaf shape
            ctx.beginPath();
            ctx.ellipse(0, 0, this.size * 2, this.size, 0, 0, 2 * Math.PI);
            ctx.fillStyle = this.color;
            ctx.fill();
            
            ctx.restore();
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < 60; i++) {
            particles.push(new Particle());
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        
        requestAnimationFrame(animateParticles);
    }

    initParticles();
    animateParticles();

    // --- 2. Form Handling & Loading State ---
    const form = document.getElementById('detectionForm');
    const fileInput = document.getElementById('fileInput');
    const fileNameDisplay = document.getElementById('fileName');
    const btn = document.querySelector('.btn-animated');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Show filename when selected
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileNameDisplay.textContent = `Selected: ${this.files[0].name}`;
        }
    });

    // Handle Submit
    form.addEventListener('submit', function(e) {
        // Note: In a real Flask app, you might want to prevent default 
        // and use AJAX, but for this template, we simulate the loading 
        // before the page reloads.
        
        // If you are using AJAX, uncomment the lines below:
        // e.preventDefault();
        // btn.classList.add('loading');
        
        // Simulate loading delay for visual effect
        btn.classList.add('loading');
        
        // If the server returns immediately, the page reloads. 
        // If you want to keep the page open, you need to handle the response via JS.
        // For now, we let the form submit naturally, but the button shows the spinner.
    });
});