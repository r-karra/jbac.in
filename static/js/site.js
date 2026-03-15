const menuToggle = document.querySelector('[data-menu-toggle]');
const menu = document.querySelector('[data-menu]');

if (menuToggle && menu) {
    menuToggle.addEventListener('click', () => {
        const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', String(!expanded));
        menu.classList.toggle('open');
    });
}

const revealItems = document.querySelectorAll('[data-reveal]');

if ('IntersectionObserver' in window && revealItems.length) {
    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12 }
    );

    revealItems.forEach(item => observer.observe(item));
} else {
    revealItems.forEach(item => item.classList.add('revealed'));
}

const songCards = document.querySelectorAll('[data-song-detail-url]');

if (songCards.length) {
    const shouldIgnoreNavigationTarget = target => {
        return Boolean(target.closest('a, button, input, select, textarea, label'));
    };

    songCards.forEach(card => {
        const destination = card.dataset.songDetailUrl;
        if (!destination) {
            return;
        }

        card.addEventListener('click', event => {
            if (shouldIgnoreNavigationTarget(event.target)) {
                return;
            }
            window.location.href = destination;
        });

        card.addEventListener('keydown', event => {
            if (event.key !== 'Enter' && event.key !== ' ') {
                return;
            }
            event.preventDefault();
            window.location.href = destination;
        });
    });
}