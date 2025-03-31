/**
 * Format price with currency
 * @param {number} price - Price value to format
 * @param {string} currency - Currency code (default: 'EUR')
 * @returns {string} Formatted price string
 */
export function formatPrice(price, currency = 'EUR') {
    if (!price) return 'Price not available';
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: currency
    }).format(price);
}
