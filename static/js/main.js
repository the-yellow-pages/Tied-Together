// Current candidate data
let currentCandidate = null;
let currentImageIndex = 0;
import { formatPrice } from '/static/js/tool/formatters.js';

const wordCard = document.getElementById('word-display');
const candidateWordElement = document.getElementById('candidate-word');
const candidateIdElement = document.getElementById('candidate-id');
const feedbackElement = document.getElementById('swipe-feedback');
const carImageElement = document.getElementById('car-img');
const carPriceElement = document.getElementById('car-price');
const carSpecsElement = document.getElementById('car-specs');
const carLocationElement = document.getElementById('car-location');

// Fetch the first car on page load
document.addEventListener('DOMContentLoaded', () => {
    getNextCandidate();
});

// Function to handle image navigation
function navigateImages(direction) {
    if (!currentCandidate || !currentCandidate.all_images || currentCandidate.all_images.length <= 1) {
        return; // Do nothing if there are no images or only one image
    }

    // Calculate new index with wraparound
    if (direction === 'next') {
        currentImageIndex = (currentImageIndex + 1) % currentCandidate.all_images.length;
    } else {
        currentImageIndex = (currentImageIndex - 1 + currentCandidate.all_images.length) % currentCandidate.all_images.length;
    }

    // Update the image source
    carImageElement.src = currentCandidate.all_images[currentImageIndex];

    // Show navigation indicators
    updateImageCounter();
}

// Update image counter display
function updateImageCounter() {
    if (currentCandidate && currentCandidate.all_images && currentCandidate.all_images.length > 1) {
        const counterElement = document.getElementById('image-counter');
        if (counterElement) {
            counterElement.textContent = `${currentImageIndex + 1}/${currentCandidate.all_images.length}`;
            counterElement.style.display = 'block';
        }
    } else {
        const counterElement = document.getElementById('image-counter');
        if (counterElement) {
            counterElement.style.display = 'none';
        }
    }
}

// Get next candidate
async function getNextCandidate() {
    try {
        // Show loading state
        candidateWordElement.textContent = "Loading...";
        candidateIdElement.textContent = "";
        carImageElement.src = "";
        carPriceElement.textContent = "";
        carSpecsElement.textContent = "";
        carLocationElement.textContent = "";
        wordCard.classList.remove('swiped-left', 'swiped-right', 'flash-red', 'flash-green');

        const response = await fetch('/api/getnextcandidate');
        const data = await response.json();

        if (data.status !== 'success' || !data.candidate) {
            throw new Error('Failed to get car data');
        }

        currentCandidate = data.candidate;
        currentImageIndex = 0; // Reset image index for new candidate

        // Display the car information
        candidateWordElement.textContent = currentCandidate.title || 'Car details not available';
        candidateIdElement.textContent = `ID: ${currentCandidate.id}`;

        // Set car image if available
        if (currentCandidate.image_url) {
            carImageElement.src = currentCandidate.image_url;
            carImageElement.alt = currentCandidate.title || 'Car image';

            // If there are multiple images, add the navigation overlay
            if (currentCandidate.all_images && currentCandidate.all_images.length > 1) {
                document.getElementById('left-nav').style.display = 'block';
                document.getElementById('right-nav').style.display = 'block';
                updateImageCounter();
            } else {
                document.getElementById('left-nav').style.display = 'none';
                document.getElementById('right-nav').style.display = 'none';
                document.getElementById('image-counter').style.display = 'none';
            }
        } else {
            carImageElement.src = '/static/img/no-image.jpg';
            carImageElement.alt = 'No image available';
            document.getElementById('left-nav').style.display = 'none';
            document.getElementById('right-nav').style.display = 'none';
            document.getElementById('image-counter').style.display = 'none';
        }

        // Set car details
        carPriceElement.textContent = formatPrice(currentCandidate.price, currentCandidate.currency);

        // Compile car specs
        let specs = [];
        if (currentCandidate.first_registration) specs.push(`Reg: ${currentCandidate.first_registration}`);
        if (currentCandidate.mileage) specs.push(currentCandidate.mileage);
        if (currentCandidate.fuel_type) specs.push(currentCandidate.fuel_type);
        if (currentCandidate.transmission) specs.push(currentCandidate.transmission);
        if (currentCandidate.body_type) specs.push(currentCandidate.body_type);

        carSpecsElement.textContent = specs.join(' • ');
        carLocationElement.textContent = currentCandidate.location ? `📍 ${currentCandidate.location}` : '';

        feedbackElement.textContent = '';

        // Animate the card entrance
        wordCard.classList.add('card-entrance');
        setTimeout(() => {
            wordCard.classList.remove('card-entrance');
        }, 500);
    } catch (error) {
        console.error('Error:', error);
        candidateWordElement.textContent = "Error loading car data";
        feedbackElement.textContent = 'Failed to fetch next car';
    }
}

// Like/Right swipe
async function likeWord() {
    if (!currentCandidate) return;

    try {
        // Flash green before swiping
        wordCard.classList.add('flash-green');

        // Wait for the flash animation to complete
        setTimeout(() => {
            // Then animate card swipe right
            wordCard.classList.remove('flash-green');
            wordCard.classList.add('swiped-right');

            // Make API request
            fetch('/api/goodswipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({
                    candidateId: currentCandidate.id,
                    action: 'like'
                })
            })
                .then(response => response.json())
                .then(data => {
                    feedbackElement.innerHTML = `<span class="liked">Liked: ${currentCandidate.title || 'this car'}</span>`;

                    // Wait for animation to complete before getting next word
                    setTimeout(getNextCandidate, 500);
                })
                .catch(error => {
                    console.error('Error:', error);
                    feedbackElement.textContent = 'Error recording like';
                });
        }, 300); // Match the flash animation duration
    } catch (error) {
        console.error('Error:', error);
        feedbackElement.textContent = 'Error recording like';
    }
}

// Dislike/Left swipe
async function dislikeWord() {
    if (!currentCandidate) return;

    try {
        // Flash red before swiping
        wordCard.classList.add('flash-red');

        // Wait for the flash animation to complete
        setTimeout(() => {
            // Then animate card swipe left
            wordCard.classList.remove('flash-red');
            wordCard.classList.add('swiped-left');

            // Make API request
            fetch('/api/badswipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({
                    candidateId: currentCandidate.id,
                    action: 'dislike'
                })
            })
                .then(response => response.json())
                .then(data => {
                    feedbackElement.innerHTML = `<span class="disliked">Disliked: ${currentCandidate.title || 'this car'}</span>`;

                    // Wait for animation to complete before getting next word
                    setTimeout(getNextCandidate, 500);
                })
                .catch(error => {
                    console.error('Error:', error);
                    feedbackElement.textContent = 'Error recording dislike';
                });
        }, 300); // Match the flash animation duration
    } catch (error) {
        console.error('Error:', error);
        feedbackElement.textContent = 'Error recording dislike';
    }
}

// Add touch swipe functionality with color flashes
let touchStartX = 0;
let touchEndX = 0;
let isDragging = false;
let dragAmount = 0;

// Touch events for mobile
wordCard.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
    isDragging = true;
});

wordCard.addEventListener('touchmove', e => {
    if (!isDragging) return;

    const currentX = e.changedTouches[0].screenX;
    dragAmount = currentX - touchStartX;

    // Apply some rotation and movement as user drags
    const rotation = dragAmount * 0.1; // Subtle rotation effect
    const opacity = Math.min(Math.abs(dragAmount) / 100, 0.5);

    wordCard.style.transform = `translateX(${dragAmount * 0.8}px) rotate(${rotation}deg)`;

    // Change background color based on drag direction
    if (dragAmount > 0) { // Right drag - like
        wordCard.style.backgroundColor = `rgba(46, 204, 113, ${opacity})`;
    } else if (dragAmount < 0) { // Left drag - dislike
        wordCard.style.backgroundColor = `rgba(231, 76, 60, ${opacity})`;
    }
});

wordCard.addEventListener('touchend', e => {
    isDragging = false;
    touchEndX = e.changedTouches[0].screenX;

    // Reset inline styles
    wordCard.style.transform = '';
    wordCard.style.backgroundColor = '';

    handleSwipe();
});

// Mouse events for desktop
wordCard.addEventListener('mousedown', e => {
    touchStartX = e.clientX;
    isDragging = true;
    e.preventDefault(); // Prevent text selection while dragging
});

document.addEventListener('mousemove', e => {
    if (!isDragging) return;

    const currentX = e.clientX;
    dragAmount = currentX - touchStartX;

    // Apply some rotation and movement as user drags
    const rotation = dragAmount * 0.1; // Subtle rotation effect
    const opacity = Math.min(Math.abs(dragAmount) / 100, 0.5);

    wordCard.style.transform = `translateX(${dragAmount * 0.8}px) rotate(${rotation}deg)`;

    // Change background color based on drag direction
    if (dragAmount > 0) { // Right drag - like
        wordCard.style.backgroundColor = `rgba(46, 204, 113, ${opacity})`;
    } else if (dragAmount < 0) { // Left drag - dislike
        wordCard.style.backgroundColor = `rgba(231, 76, 60, ${opacity})`;
    }
});

document.addEventListener('mouseup', e => {
    if (!isDragging) return;

    isDragging = false;
    touchEndX = e.clientX;

    // Reset inline styles
    wordCard.style.transform = '';
    wordCard.style.backgroundColor = '';

    handleSwipe();
});

function handleSwipe() {
    const SWIPE_THRESHOLD = 50;
    if (touchEndX < touchStartX - SWIPE_THRESHOLD) {
        // Swiped left
        dislikeWord();
    } else if (touchEndX > touchStartX + SWIPE_THRESHOLD) {
        // Swiped right
        likeWord();
    }
}

// Keyboard navigation
document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') {
        dislikeWord();
    } else if (e.key === 'ArrowRight') {
        likeWord();
    }
});

// Get CSRF token from cookies
function getCsrfToken() {
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

// Add button event listeners
document.getElementById('like-btn').addEventListener('click', likeWord);
document.getElementById('dislike-btn').addEventListener('click', dislikeWord);

// Add image navigation event listenersd event listener and merge its content
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners for image navigation
    document.getElementById('left-nav').addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering card swipe
        navigateImages('prev');
    });

    document.getElementById('right-nav').addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering card swipe
        navigateImages('next');
    });

    getNextCandidate();
});
