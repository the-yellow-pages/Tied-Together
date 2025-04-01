// Fetch the next candidate from the API
export async function fetchNextCandidate() {
    try {
        const response = await fetch('/api/getnextcandidate');
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

// Record a like action for a candidate
export async function recordLike(user, candidateId) {
    try {
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
            }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error recording like:', error);
        throw error;
    }
}

// Record a dislike action for a candidate
export async function recordDislike(candidateId) {
    try {
        const response = await fetch('/api/badswipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                candidateId,
                action: 'dislike',
            }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error recording dislike:', error);
        throw error;
    }
}

// Get CSRF token from cookies
function getCsrfToken() {
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}
