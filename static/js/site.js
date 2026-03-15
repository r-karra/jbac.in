const menuToggle = document.querySelector('[data-menu-toggle]');
const menu = document.querySelector('[data-menu]');

if (menuToggle && menu) {
    menuToggle.addEventListener('click', () => {
        const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', String(!expanded));
        menu.classList.toggle('open');
        if (expanded) {
            document.querySelectorAll('.nav-dropdown.open').forEach(dropdown => {
                dropdown.classList.remove('open');
                const trigger = dropdown.querySelector('[data-nav-dropdown-trigger]');
                if (trigger) {
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });
        }
    });
}

const navDropdownTriggers = document.querySelectorAll('[data-nav-dropdown-trigger]');
const compactNavQuery = window.matchMedia('(max-width: 980px)');

const closeOtherDropdowns = current => {
    document.querySelectorAll('.nav-dropdown.open').forEach(dropdown => {
        if (current && dropdown === current) {
            return;
        }
        dropdown.classList.remove('open');
        const trigger = dropdown.querySelector('[data-nav-dropdown-trigger]');
        if (trigger) {
            trigger.setAttribute('aria-expanded', 'false');
        }
    });
};

if (navDropdownTriggers.length) {
    navDropdownTriggers.forEach(trigger => {
        trigger.addEventListener('click', event => {
            if (!compactNavQuery.matches) {
                return;
            }

            const dropdown = trigger.closest('.nav-dropdown');
            if (!dropdown) {
                return;
            }

            const isOpen = dropdown.classList.contains('open');
            if (!isOpen) {
                event.preventDefault();
                closeOtherDropdowns(dropdown);
                dropdown.classList.add('open');
                trigger.setAttribute('aria-expanded', 'true');
            }
        });
    });

    document.addEventListener('click', event => {
        if (!compactNavQuery.matches) {
            return;
        }
        if (event.target.closest('.nav-dropdown') || event.target.closest('[data-menu-toggle]')) {
            return;
        }
        closeOtherDropdowns(null);
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