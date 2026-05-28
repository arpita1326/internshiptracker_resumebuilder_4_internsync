// ==========================================
// INTERSYNC PROFESSIONAL SCRIPT
// ==========================================

// Smooth page animation

window.addEventListener("load", () => {
    document.body.classList.add("loaded");
});

// ==========================================
// AUTO CLOSE ALERTS
// ==========================================

setTimeout(() => {

    const alerts = document.querySelectorAll(".error-box");

    alerts.forEach(alert => {

        alert.style.opacity = "0";

        setTimeout(() => {
            alert.style.display = "none";
        }, 500);

    });

}, 4000);

// ==========================================
// CONFIRM DELETE
// ==========================================

const deleteButtons = document.querySelectorAll(".delete-btn");

deleteButtons.forEach(button => {

    button.addEventListener("click", (e) => {

        const confirmDelete = confirm(
            "Are you sure you want to delete this internship?"
        );

        if (!confirmDelete) {
            e.preventDefault();
        }

    });

});

// ==========================================
// FORM INPUT ANIMATION
// ==========================================

const inputs = document.querySelectorAll("input, textarea, select");

inputs.forEach(input => {

    input.addEventListener("focus", () => {
        input.style.transform = "scale(1.01)";
    });

    input.addEventListener("blur", () => {
        input.style.transform = "scale(1)";
    });

});

// ==========================================
// PASSWORD TOGGLE
// ==========================================

const passwordInputs = document.querySelectorAll(
    'input[type="password"]'
);

passwordInputs.forEach(password => {

    const wrapper = document.createElement("div");

    wrapper.style.position = "relative";

    password.parentNode.insertBefore(wrapper, password);

    wrapper.appendChild(password);

    const icon = document.createElement("i");

    icon.className = "fa-solid fa-eye";

    icon.style.position = "absolute";

    icon.style.right = "15px";

    icon.style.top = "50%";

    icon.style.transform = "translateY(-50%)";

    icon.style.color = "#94a3b8";

    icon.style.cursor = "pointer";

    wrapper.appendChild(icon);

    icon.addEventListener("click", () => {

        if (password.type === "password") {

            password.type = "text";

            icon.classList.remove("fa-eye");

            icon.classList.add("fa-eye-slash");

        } else {

            password.type = "password";

            icon.classList.remove("fa-eye-slash");

            icon.classList.add("fa-eye");

        }

    });

});

// ==========================================
// BUTTON RIPPLE EFFECT
// ==========================================

const buttons = document.querySelectorAll("button, .btn");

buttons.forEach(button => {

    button.addEventListener("click", function (e) {

        const ripple = document.createElement("span");

        ripple.classList.add("ripple");

        this.appendChild(ripple);

        const x = e.clientX - e.target.offsetLeft;

        const y = e.clientY - e.target.offsetTop;

        ripple.style.left = `${x}px`;

        ripple.style.top = `${y}px`;

        setTimeout(() => {
            ripple.remove();
        }, 600);

    });

});

// ==========================================
// SCROLL ANIMATION
// ==========================================

const revealElements = document.querySelectorAll(
    ".stats-card, .internship-card, .table-box, .analytics-box"
);

window.addEventListener("scroll", () => {

    revealElements.forEach(element => {

        const windowHeight = window.innerHeight;

        const revealTop = element.getBoundingClientRect().top;

        if (revealTop < windowHeight - 80) {

            element.classList.add("active-reveal");

        }

    });

});

// ==========================================
// SEARCH FILTER ANIMATION
// ==========================================

const searchInput = document.querySelector(
    'input[name="search"]'
);

if (searchInput) {

    searchInput.addEventListener("keyup", () => {

        searchInput.style.boxShadow =
            "0 0 15px rgba(59,130,246,0.4)";

    });

}

// ==========================================
// SUCCESS MESSAGE
// ==========================================

const urlParams = new URLSearchParams(window.location.search);

if (urlParams.get("success")) {

    const successBox = document.createElement("div");

    successBox.className = "success-toast";

    successBox.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        Action completed successfully!
    `;

    document.body.appendChild(successBox);

    setTimeout(() => {
        successBox.classList.add("show-toast");
    }, 100);

    setTimeout(() => {

        successBox.classList.remove("show-toast");

        setTimeout(() => {
            successBox.remove();
        }, 500);

    }, 3000);

}

// ==========================================
// DARK MODE EFFECT
// ==========================================

const cards = document.querySelectorAll(
    ".stats-card, .internship-card, .profile-card"
);

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-6px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px)";

    });

});

// ==========================================
// LOADING BUTTON EFFECT
// ==========================================

const forms = document.querySelectorAll("form");

forms.forEach(form => {

    form.addEventListener("submit", () => {

        const submitBtn = form.querySelector(
            'button[type="submit"]'
        );

        if (submitBtn) {

            submitBtn.innerHTML = `
                <i class="fa-solid fa-spinner fa-spin me-2"></i>
                Processing...
            `;

            submitBtn.disabled = true;

        }

    });

});