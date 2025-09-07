document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".alert");
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = "0";
            msg.style.transition = "opacity 0.5s ease";
            setTimeout(() => msg.remove(), 500);
        }, 3000); // desaparece a los 3 segundos
    });
});
