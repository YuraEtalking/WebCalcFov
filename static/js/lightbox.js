
const lightbox = document.querySelector('#lightbox');
const lightboxImage = lightbox.querySelector('.lightbox__image');
const closeButton = lightbox.querySelector('.lightbox__close');

let scale = 1;
let translateX = 0;
let translateY = 0;
let isDragging = false;
let startX = 0;
let startY = 0;

function updateImageTransform() {
    lightboxImage.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;

    if (scale > 1) {
        lightboxImage.classList.add('is-zoomed');
    } else {
        lightboxImage.classList.remove('is-zoomed');
    }
}

function resetZoom() {
    scale = 1;
    translateX = 0;
    translateY = 0;
    isDragging = false;
    lightboxImage.classList.remove('is-zoomed', 'is-dragging');
    updateImageTransform();
}

document.querySelectorAll('.gallery-item').forEach((button) => {
    button.addEventListener('click', () => {
        const image = button.querySelector('img');

        resetZoom();

        lightboxImage.src = button.dataset.full;
        lightboxImage.alt = image.alt;
        lightbox.hidden = false;
    });
});

function closeLightbox() {
    lightbox.hidden = true;
    lightboxImage.src = '';
    resetZoom();
}

closeButton.addEventListener('click', closeLightbox);

lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
        closeLightbox();
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !lightbox.hidden) {
        closeLightbox();
    }
});

lightboxImage.addEventListener('wheel', (event) => {
    event.preventDefault();

    const rect = lightboxImage.getBoundingClientRect();

    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    const imageCenterX = rect.width / 2;
    const imageCenterY = rect.height / 2;

    const pointX = mouseX - imageCenterX;
    const pointY = mouseY - imageCenterY;

    const oldScale = scale;

    if (event.deltaY < 0) {
        scale *= 1.15;
    } else {
        scale /= 1.15;
    }

    scale = Math.min(Math.max(scale, 1), 5);

    const scaleRatio = scale / oldScale;

    translateX = event.clientX - window.innerWidth / 2 -
        (event.clientX - window.innerWidth / 2 - translateX) * scaleRatio;

    translateY = event.clientY - window.innerHeight / 2 -
        (event.clientY - window.innerHeight / 2 - translateY) * scaleRatio;

    if (scale === 1) {
        translateX = 0;
        translateY = 0;
    }

    lightboxImage.classList.toggle('is-zoomed', scale > 1);

    updateImageTransform();
});

lightboxImage.addEventListener('mousedown', (event) => {
    if (scale <= 1) {
        return;
    }

    isDragging = true;
    startX = event.clientX - translateX;
    startY = event.clientY - translateY;

    lightboxImage.classList.add('is-dragging');
});

document.addEventListener('mousemove', (event) => {
    if (!isDragging) {
        return;
    }

    translateX = event.clientX - startX;
    translateY = event.clientY - startY;

    updateImageTransform();
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    lightboxImage.classList.remove('is-dragging');
});

lightboxImage.addEventListener('dblclick', () => {
    if (scale === 1) {
        scale = 2;
    } else {
        resetZoom();
    }

    updateImageTransform();
});