document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const menu = toggle.nextElementSibling;
            const isOpen = menu.classList.contains('show');

            dropdownMenus.forEach(m => m.classList.remove('show'));
            dropdownToggles.forEach(t => t.classList.remove('active'));

            if (!isOpen) {
                menu.classList.add('show');
                toggle.classList.add('active');
            }
        });
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            dropdownMenus.forEach(m => m.classList.remove('show'));
            dropdownToggles.forEach(t => t.classList.remove('active'));
        }
    });

    dropdownMenus.forEach(menu => {
        menu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });

    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = toggle.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            const eyeIcon = toggle.querySelector('.eye-open');
            const eyeClosedIcon = toggle.querySelector('.eye-closed');
            if (eyeIcon && eyeClosedIcon) {
                eyeIcon.style.display = type === 'password' ? 'block' : 'none';
                eyeClosedIcon.style.display = type === 'password' ? 'none' : 'block';
            }
        });
    });

    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('.input-field');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });

            input.addEventListener('input', () => {
                if (input.classList.contains('error') && input.value.trim()) {
                    input.classList.remove('error');
                }
            });
        });
    });

    const flashMessages = document.querySelectorAll('.message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });

    const charts = document.querySelectorAll('canvas[id$="Chart"]');
    charts.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        if (ctx) {
            const originalFillText = ctx.fillText.bind(ctx);
            ctx.fillText = function(text, x, y, maxWidth) {
                this.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim() || '#f5f5f7';
                return originalFillText(text, x, y, maxWidth);
            };
        }
    });
});