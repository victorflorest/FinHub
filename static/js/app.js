document.querySelectorAll('[data-bs-toggle="collapse"]').forEach((button) => {
    const targetSelector = button.getAttribute('data-bs-target');
    const target = targetSelector ? document.querySelector(targetSelector) : null;

    if (!target) {
        return;
    }

    button.addEventListener('click', () => {
        const isExpanded = button.getAttribute('aria-expanded') === 'true';

        button.setAttribute('aria-expanded', String(!isExpanded));
        target.classList.toggle('show', !isExpanded);
    });
});
