const { defineConfig } = require("cypress");

module.exports = defineConfig({
    e2e: {
        // ESTA LÍNEA ES VITAL: Le dice a Cypress dónde está tu servidor de Django
        baseUrl: 'http://localhost:8000',

        video: true,
        setupNodeEvents(on, config) {
            on("before:browser:launch", (browser = {}, launchOptions) => {
                if (browser.name === "firefox") {
                    // Excelente optimización para Linux/CI
                    launchOptions.preferences["layers.acceleration.disabled"] = true;
                }
                return launchOptions;
            });
        },
    },
    // Configuración del reporte Mochawesome
    reporter: "mochawesome",
    reporterOptions: {
        reportDir: "cypress/reports",
        overwrite: false,
        html: true,
        json: true,
    },
});
