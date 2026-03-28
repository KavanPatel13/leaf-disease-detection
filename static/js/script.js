document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("bg-particles");

    if (canvas) {
        const ctx = canvas.getContext("2d");
        let particles = [];
        const colors = ["#22c55e", "#4ade80", "#16a34a", "#86efac", "#bbf7d0"];

        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        const drawLeaf = (x, y, size, rotation, color, opacity) => {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(rotation);
            ctx.globalAlpha = opacity;
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(size * 0.5, -size * 0.3, size, 0, 0, size * 1.5);
            ctx.bezierCurveTo(-size, 0, -size * 0.5, -size * 0.3, 0, 0);
            ctx.fill();

            ctx.strokeStyle = "rgba(255,255,255,0.4)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(0, size * 1.2);
            ctx.stroke();
            ctx.restore();
        };

        class LeafParticle {
            constructor() {
                this.reset();
            }

            reset() {
                this.x = Math.random() * canvas.width;
                this.y = canvas.height + Math.random() * 100;
                this.size = Math.random() * 10 + 4;
                this.speedY = Math.random() * 1 + 0.3;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                this.opacity = Math.random() * 0.5 + 0.3;
                this.rotation = Math.random() * Math.PI * 2;
                this.rotationSpeed = (Math.random() - 0.5) * 0.02;
            }

            update() {
                this.y -= this.speedY;
                this.x += this.speedX;
                this.rotation += this.rotationSpeed;

                if (this.y < -50) {
                    this.reset();
                    this.x = Math.random() * canvas.width;
                }
            }

            draw() {
                drawLeaf(this.x, this.y, this.size, this.rotation, this.color, this.opacity);
            }
        }

        const initParticles = () => {
            particles = [];

            for (let i = 0; i < 60; i += 1) {
                particles.push(new LeafParticle());
            }
        };

        const animateParticles = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((particle) => {
                particle.update();
                particle.draw();
            });
            requestAnimationFrame(animateParticles);
        };

        window.addEventListener("resize", resizeCanvas);
        resizeCanvas();
        initParticles();
        animateParticles();
    }

    const revealElements = document.querySelectorAll(".reveal");

    if (revealElements.length) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15 }
        );

        revealElements.forEach((element) => observer.observe(element));
    }

    const pageLinks = document.querySelectorAll("[data-page-link='true']");
    pageLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            if (
                event.defaultPrevented ||
                event.button !== 0 ||
                event.metaKey ||
                event.ctrlKey ||
                event.shiftKey ||
                event.altKey
            ) {
                return;
            }

            const href = link.getAttribute("href");
            if (!href || href.startsWith("#")) {
                return;
            }

            event.preventDefault();
            document.body.classList.add("is-leaving");
            window.setTimeout(() => {
                window.location.href = href;
            }, 120);
        });
    });

    const form = document.getElementById("detectionForm");
    const fileInput = document.getElementById("fileInput");
    const fileNameDisplay = document.getElementById("fileName");
    const loadingOverlay = document.getElementById("loadingOverlay");
    const submitButton = form ? form.querySelector("button[type='submit'].btn-animated") : null;

    if (form && fileInput && fileNameDisplay) {
        fileInput.addEventListener("change", function () {
            if (this.files && this.files[0]) {
                fileNameDisplay.textContent = `Selected: ${this.files[0].name}`;
            } else {
                fileNameDisplay.textContent = "";
            }
        });

        form.addEventListener("submit", () => {
            if (submitButton) {
                submitButton.classList.add("loading");
                submitButton.disabled = true;
            }

            if (loadingOverlay) {
                loadingOverlay.classList.remove("d-none");
            }
        });
    }
});
