// Load Telegram WebApp script dynamically
export function loadTelegramScript(tg) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://telegram.org/js/telegram-web-app.js';
        script.onload = () => {
            tg = window.Telegram?.WebApp;
            resolve(tg);
        };
        script.onerror = () => reject(new Error('Failed to load Telegram WebApp script'));
        document.head.appendChild(script);
    });
}

// Initialize Telegram WebApp
export function initTelegramWebApp(tg, telegramConnected) {
    if (tg && tg.initDataUnsafe?.query_id) {
        telegramConnected = true;
        console.log("Telegram WebApp initialized successfully");

        // Expand the WebApp to fullscreen
        tg.expand();

        // Change theme based on Telegram color scheme
        if (tg.colorScheme === 'dark') {
            document.body.classList.add('dark-theme');
        }

        // Setup the main button for actions if needed
        setupTelegramMainButton(tg, telegramConnected);

        // Notify Telegram that the WebApp is ready
        tg.ready();
    } else {
        console.log("Telegram WebApp not available or not running inside Telegram");
    }
}

// Setup Telegram Main Button
function setupTelegramMainButton(tg, telegramConnected) {
    if (!telegramConnected) return;

    // Configure the main button
    tg.MainButton.setParams({
        text: 'SHARE FAVORITE CAR',
        color: '#31b545',
        text_color: '#ffffff',
        is_visible: true
    });

    // Add event listener for the main button
    tg.MainButton.onClick(shareFavoriteCar);
}

// Function to share the currently liked car with Telegram
// A <sendData> method used to send data to the bot. When this method is called, a service message is sent to the bot containing the data data of the length up to 4096 bytes, and the Mini App is closed. See the field web_app_data in the class Message.
// This method is only available for Mini Apps launched via a Keyboard button.
export function shareFavoriteCar(tg, telegramConnected, currentCandidate) {
    if (!telegramConnected || !currentCandidate) {
        console.log("Cannot share: Telegram not connected or no car selected");
        return;
    }

    // Prepare data to send back to the Telegram Bot
    const carData = {
        id: currentCandidate.id,
        title: currentCandidate.title,
        price: currentCandidate.price,
        currency: currentCandidate.currency,
        image_url: currentCandidate.image_url
    };


    // Send data back to Telegram
    tg.sendData(JSON.stringify(carData));
}

export function getUserInfo(tg) {
    if (!tg) {
        console.error("Telegram WebApp is not initialized");
        return null;
    }
    try {
        const { id, first_name, last_name, username } = window.Telegram.WebApp.initDataUnsafe.user;
        return {
            id,
            first_name,
            last_name,
            username
        };
    } catch (error) {
        console.error("Error retrieving user info:", error);
        return null;
    }
}
