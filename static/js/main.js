// Current candidate data
let currentCandidate = null;
let currentImageIndex = 0;
import { formatPrice } from '/static/js/tool/formatters.js';
import { loadTelegramScript, initTelegramWebApp, getUserInfo } from '/static/js/tool/telegram.js'
import { fetchNextCandidate, recordLike, recordDislike, fetchLikedVehicles, authorizeWithTelegram, removeLike } from '/static/js/tool/api.js';

let tg = null;
let telegramConnected = false;
let tgUser = null;
// Pagination state for liked vehicles
let currentPage = 1;
let totalPages = 1;
let itemsPerPage = 5;

const wordCard = document.getElementById('word-display');
const candidateWordElement = document.getElementById('candidate-word');
const candidateIdElement = document.getElementById('candidate-id');
const feedbackElement = document.getElementById('swipe-feedback');
const carImageElement = document.getElementById('car-img');
const carPriceElement = document.getElementById('car-price');
const carSpecsElement = document.getElementById('car-specs');
const carLocationElement = document.getElementById('car-location');

// Fetch the first car on page load
document.addEventListener('DOMContentLoaded', async () => {
    tg = undefined;
    try {
        tg = await loadTelegramScript(tg)
        if (tg.initData) {
            telegramConnected = true; // Set the flag to true when connected
        } else {
            console.log("Telegram not found");
            telegramConnected = false; // Set the flag to false if user info is not available
        }
    } catch (error) {
        console.error("Error loading Telegram script:", error);
    }
    if (telegramConnected) {
        initTelegramWebApp(tg, telegramConnected);
        console.log("Telegram loaded");
        tgUser = getUserInfo(tg);
        console.log("USER", tgUser);
        // Set the greeting based on user info
    }
    else {
        console.log("telegram not loaded");
    }
    updateGreeting();
    // Setup modal listeners
    setupModalListeners();
    getNextCandidate(tgUser);
});

// Function to update the greeting based on user info
function updateGreeting() {
    const greetingElement = document.getElementById('greeting');
    if (greetingElement) {
        if (tgUser && tgUser.id) {
            greetingElement.innerHTML = `Hello <span class="username">@${tgUser.username || tgUser.first_name || tgUser.id}</span>! Welcome to Car Tinder!`;
            greetingElement.classList.add('user-greeting');
        } else {
            greetingElement.innerHTML = 'For the best experience, please open this app in <a href="https://telegram.org/" target="_blank">Telegram</a>!';
            greetingElement.classList.add('telegram-invite');
        }
    }
}

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
    carImageElement.src = currentCanidate.all_images[currentImageIndex];

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
async function getNextCandidate(user) {
    try {
        // Show loading state
        candidateWordElement.textContent = "Loading...";
        candidateIdElement.textContent = "";
        carImageElement.src = "";
        carPriceElement.textContent = "";
        carSpecsElement.textContent = "";
        carLocationElement.textContent = "";
        wordCard.classList.remove('swiped-left', 'swiped-right', 'flash-red', 'flash-green');

        currentCandidate = await fetchNextCandidate(user);
        currentImageIndex = 0; // Reset image index for new candidate

        // Display the car information
        if (currentCandidate.source_link) {
            // Display title as a link if source_link is available
            candidateWordElement.innerHTML = `<a href="${currentCandidate.source_link}" target="_blank">${currentCandidate.title || 'Car details not available'}</a>`;
        } else {
            candidateWordElement.textContent = currentCandidate.title || 'Car details not available';
        }
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
        setTimeout(async () => {
            // Then animate card swipe right
            wordCard.classList.remove('flash-green');
            wordCard.classList.add('swiped-right');

            // Make API request
            if (telegramConnected) {
                await recordLike(tgUser, currentCandidate.id, tg?.initData);
            }
            feedbackElement.innerHTML = `<span class="liked">Liked: ${currentCandidate.title || 'this car'}</span>`;

            // Wait for animation to complete before getting next word
            setTimeout(getNextCandidate, 500);
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
        setTimeout(async () => {
            // Then animate card swipe left
            wordCard.classList.remove('flash-red');
            wordCard.classList.add('swiped-left');

            // Make API request if connected to Telegram
            if (telegramConnected) {
                await recordDislike(tgUser, currentCandidate.id, tg?.initData);
            }
            feedbackElement.innerHTML = `<span class="disliked">Disliked: ${currentCandidate.title || 'this car'}</span>`;
            // Wait for animation to complete before getting next word
            setTimeout(getNextCandidate, 500);
        }, 300); // Match the flash animation duration
    } catch (error) {
        console.error('Error:', error);
        feedbackElement.textContent = 'Error recording dislike';
    }
}

// Share the current car through Telegram
function shareCurrentCar() {
    if (currentCandidate && telegramConnected) {
        shareFavoriteCar(tg, telegramConnected, currentCandidate);
        feedbackElement.innerHTML = `<span class="shared">Shared: ${currentCandidate.title || 'this car'}</span>`;
    } else {
        feedbackElement.textContent = 'No car to share';
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
document.getElementById('favorites-btn').addEventListener('click', openLikedVehiclesModal);

// Remove the old share button listener that no longer exists and isn't needed
// document.getElementById('share-btn').addEventListener('click', shareCurrentCar);

// Fix the event listeners for image navigation - move them out of the DOMContentLoaded
// handler that would cause them to be registered twice
document.getElementById('left-nav').addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent triggering card swipe
    navigateImages('prev');
});

document.getElementById('right-nav').addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent triggering card swipe
    navigateImages('next');
});

// Clean up the duplicate DOMContentLoaded event listener that was causing conflicts
// Remove this duplicate listener that was added in the previous update
// document.addEventListener('DOMContentLoaded', () => {
//     // Add event listeners for image navigation
//     document.getElementById('left-nav').addEventListener('click', (e) => {
//         e.stopPropagation(); // Prevent triggering card swipe
//         navigateImages('prev');
//     });
// 
//     document.getElementById('right-nav').addEventListener('click', (e) => {
//         e.stopPropagation(); // Prevent triggering card swipe
//         navigateImages('next');
//     });
// 
//     getNextCandidate();
// });

// Setup modal event listeners
function setupModalListeners() {
    const modal = document.getElementById('liked-vehicles-modal');
    const favoritesBtn = document.getElementById('favorites-btn');
    const closeButton = document.querySelector('.close-modal');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    // Open modal when favorites button is clicked
    favoritesBtn.addEventListener('click', () => {
        openLikedVehiclesModal();
    });

    // Close modal when X is clicked
    closeButton.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });

    // Pagination controls
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadLikedVehicles();
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadLikedVehicles();
        }
    });
}

// Function to open the modal and load liked vehicles
async function openLikedVehiclesModal() {
    const modal = document.getElementById('liked-vehicles-modal');
    modal.classList.add('show');

    // Reset to first page when opening
    currentPage = 1;
    loadLikedVehicles();
}

// Load liked vehicles with pagination
async function loadLikedVehicles() {
    if (!tgUser) {
        showNoFavoritesMessage("Please connect with Telegram to view your favorites");
        return;
    }

    const container = document.getElementById('liked-vehicles-container');
    const pageInfo = document.getElementById('page-info');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    // Show loading state
    container.innerHTML = '<div class="loading-indicator">Loading your favorites...</div>';

    try {
        const result = await fetchLikedVehicles(tgUser.id, currentPage, itemsPerPage, tg?.initData);
        const { vehicles, totalCount } = result;

        // Calculate total pages
        totalPages = Math.ceil(totalCount / itemsPerPage);

        // Update pagination UI
        pageInfo.textContent = `Page ${currentPage} of ${totalPages || 1}`;
        prevButton.disabled = currentPage <= 1;
        nextButton.disabled = currentPage >= totalPages || totalPages === 0;

        // Display vehicles or no results message
        if (vehicles && vehicles.length > 0) {
            container.innerHTML = '';
            vehicles.forEach(vehicle => {
                container.appendChild(createVehicleCard(vehicle));
            });
        } else {
            showNoFavoritesMessage("You haven't liked any vehicles yet");
        }
    } catch (error) {
        console.error('Error loading liked vehicles:', error);
        container.innerHTML = '<div class="no-favorites">Error loading favorites. Please try again.</div>';
    }
}

// Create a vehicle card element
function createVehicleCard(vehicle) {
    const card = document.createElement('div');
    card.className = 'vehicle-card';
    card.dataset.id = vehicle.id; // Add the vehicle ID as a data attribute

    // Determine image URL (use the first image or a placeholder)
    const imageUrl = vehicle.image_url ||
        (vehicle.all_images && vehicle.all_images.length > 0 ?
            vehicle.all_images[0] : '/static/img/no-image.jpg');

    // Create HTML for vehicle card
    card.innerHTML = `
        <div class="vehicle-image" style="background-image: url('${imageUrl}')"></div>
        <div class="vehicle-details">
            <div class="vehicle-header">
                <h3 class="vehicle-title">
                    ${vehicle.source_link
            ? (`<a href="${vehicle.source_link}" target="_blank">${vehicle.title || 'Unnamed Vehicle'}</a>`)
            : (vehicle.title || 'Unnamed Vehicle')
        }
                </h3>
                <button class="remove-vehicle-btn" aria-label="Remove from favorites">×</button>
            </div>
            <p class="vehicle-price">${formatPrice(vehicle.price, vehicle.currency)}</p>
            <p class="vehicle-specs">${getVehicleSpecs(vehicle)}</p>
        </div>
    `;

    // Add event listener for the remove button
    const removeBtn = card.querySelector('.remove-vehicle-btn');
    removeBtn.addEventListener('click', async (e) => {
        e.stopPropagation(); // Prevent event bubbling
        try {
            if (confirm('Remove this vehicle from your favorites?')) {
                await removeVehicleLike(vehicle.id);
                card.classList.add('removing');
                setTimeout(() => {
                    card.remove();
                    // Check if there are no more vehicles in the container
                    const container = document.getElementById('liked-vehicles-container');
                    if (container.children.length === 0) {
                        showNoFavoritesMessage("You haven't liked any vehicles yet");
                    }
                }, 300);
            }
        } catch (error) {
            console.error('Error removing vehicle:', error);
            alert('Failed to remove vehicle from favorites');
        }
    });

    return card;
}

// Helper function to remove a vehicle like
async function removeVehicleLike(vehicleId) {
    if (!tgUser) {
        throw new Error('User not authenticated');
    }

    try {
        const result = await removeLike(tgUser, vehicleId, tg?.initData);
        if (result.status !== 'success') {
            throw new Error(result.message || 'Failed to remove like');
        }
        return result;
    } catch (error) {
        console.error('Error removing like:', error);
        throw error;
    }
}

// Helper to format vehicle specs for display
function getVehicleSpecs(vehicle) {
    let specs = [];
    if (vehicle.first_registration) specs.push(`${vehicle.first_registration}`);
    if (vehicle.mileage) specs.push(vehicle.mileage);
    if (vehicle.fuel_type) specs.push(vehicle.fuel_type);
    if (vehicle.transmission) specs.push(vehicle.transmission);

    return specs.join(' • ') || 'No specifications available';
}

// Show message when no favorites are available
function showNoFavoritesMessage(message) {
    const container = document.getElementById('liked-vehicles-container');
    container.innerHTML = `<div class="no-favorites">${message}</div>`;
}
