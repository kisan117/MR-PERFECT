const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const express = require('express');
const path = require('path');
const multer = require('multer');  // To handle file uploads
const qrcode = require('qrcode-terminal');
const http = require('http');
const socketIo = require('socket.io');
const twilio = require('twilio');  // To send SMS for pairing code

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const PORT = process.env.PORT || 3000;

const accountSid = 'your_twilio_account_sid';  // Twilio SID
const authToken = 'your_twilio_auth_token';    // Twilio Auth Token
const clientTwilio = new twilio(accountSid, authToken);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve the HTML form at the root endpoint
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Route to handle pairing
app.post('/pair', async (req, res) => {
    const ownNumber = req.body.ownNumber;
    const targetNumber = req.body.targetNumber;

    // Ensure both numbers are provided
    if (!ownNumber || !targetNumber) {
        return res.status(400).send('Both numbers are required.');
    }

    // Generate a pairing code
    const pairingCode = Math.floor(1000 + Math.random() * 9000);  // 4-digit code

    // Send the pairing code to the user's phone via SMS using Twilio
    try {
        await clientTwilio.messages.create({
            body: `Your pairing code is: ${pairingCode}`,
            from: 'your_twilio_phone_number',  // Twilio number
            to: ownNumber
        });

        console.log(`Pairing code sent to ${ownNumber}: ${pairingCode}`);
        res.send(`<h3>Pairing code sent to ${ownNumber}. Your code: ${pairingCode}</h3>`);
    } catch (error) {
        console.error('Error sending pairing code:', error);
        res.status(500).send('Error sending pairing code');
    }
});

// WhatsApp client setup
const client = new Client({
    authStrategy: new LocalAuth()
});

// QR code generation for first-time login
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    io.emit('qr', qr);  // Emit QR code to client (frontend)
    console.log('QR Code generated! Scan it in WhatsApp Web.');
});

// When the client is ready
client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
});

// Initialize the WhatsApp client
client.initialize();

// Start the Express server
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
