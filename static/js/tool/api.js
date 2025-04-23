// Fetch the next batch of candidates from the API
export async function fetchCandidates(user, options = {}) {
    try {
        const {
            limit = 10,
            startPrice = 0,
            endPrice = 0,
            startYear = 0,
            endYear = 0,
            notFuelType = null,
            fuelType = null
        } = options;

        const response = await fetch('/api/getnextcandidate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                user,
                limit,
                start_price: startPrice,
                end_price: endPrice,
                start_year: startYear,
                end_year: endYear,
                not_fuel_type: notFuelType,
                fuel_type: fuelType
            }),
        });
        const data = await response.json();
        if (data.status !== 'success' || !data.candidates) {
            throw new Error('Failed to get car data');
        }
        return data.candidates;
    } catch (error) {
        console.error('Error fetching candidates:', error);
        throw error;
    }
}

// Fetch the next candidate from the API
export async function fetchNextCandidate(user) {
    try {
        const response = await fetch('/api/getnextcandidate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                user,
            }),
        });
        const data = await response.json();
        if (data.status !== 'success' || !data.candidate) {
            throw new Error('Failed to get car data');
        }
        return data.candidate;
    } catch (error) {
        console.error('Error fetching next candidate:', error);
        throw error;
    }
}

// remove previous like
export async function removeLike(user, candidateId, initData) {
    try {
        // Parse the initData if it's a string
        const auth_object = prepareAuthData(initData);

        const response = await fetch('/api/remove_like', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                user,
                candidateId,
                action: 'remove_like',
                auth_object
            }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error removing like:', error);
        throw error;
    }
}

// Record a like action for a candidate
export async function recordLike(user, candidateId, initData) {
    try {
        // Parse the initData if it's a string
        const auth_object = prepareAuthData(initData);

        const response = await fetch('/api/goodswipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                user,
                candidateId,
                action: 'like',
                auth_object
            }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error recording like:', error);
        throw error;
    }
}

// Record a dislike action for a candidate
export async function recordDislike(user, candidateId, initData) {
    try {
        // Parse the initData if it's a string
        const auth_object = prepareAuthData(initData);

        const response = await fetch('/api/badswipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                user,
                candidateId,
                action: 'dislike',
                auth_object
            }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error recording dislike:', error);
        throw error;
    }
}

// Fetch liked vehicles with pagination
export async function fetchLikedVehicles(userId, page = 1, limit = 10, initData) {
    try {
        // Parse the initData if it's a string
        const auth_object = prepareAuthData(initData);

        const response = await fetch('/api/get_liked_vehicles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                user_id: userId,
                page: page,
                limit: limit,
                auth_object
            }),
        });

        const data = await response.json();
        if (data.status !== 'success') {
            throw new Error(data.message || 'Failed to fetch liked vehicles');
        }

        return {
            vehicles: data.liked_vehicles || [],
            totalCount: data.total_count || 0
        };
    } catch (error) {
        console.error('Error fetching liked vehicles:', error);
        throw error;
    }
}

// Authorize Telegram Mini App data
export async function authorizeWithTelegram(initData) {
    try {
        // Parse the initData query string into an object if it's a string
        let dataToSend = initData;
        if (typeof initData === 'string') {
            dataToSend = Object.fromEntries(new URLSearchParams(initData));
        }

        const response = await fetch('/api/authorize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(dataToSend),
        });

        const data = await response.json();
        if (data.status !== 'success') {
            throw new Error(data.message || 'Authorization failed');
        }

        return {
            success: true,
            user: data.user
        };
    } catch (error) {
        console.error('Error during Telegram authorization:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// Helper function to prepare auth data for API requests
export function prepareAuthData(initData) {
    let auth_object = initData;
    if (typeof initData === 'string') {
        auth_object = Object.fromEntries(new URLSearchParams(initData));
    }
    return auth_object;
}

// Get CSRF token from cookies
function getCsrfToken() {
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}
