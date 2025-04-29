const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./messages.db', (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to the database.');
    }
});

// Table creation for messages queue
db.run('CREATE TABLE IF NOT EXISTS messages_queue (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, message TEXT, status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)');

// Insert new message into queue
function addMessageToQueue(number, message) {
    const stmt = db.prepare('INSERT INTO messages_queue (number, message, status) VALUES (?, ?, ?)');
    stmt.run(number, message, 'pending', function(err) {
        if (err) {
            console.error('Error inserting message into queue:', err.message);
        } else {
            console.log(`Message added to queue: ${message}`);
        }
    });
    stmt.finalize();
}

// Retrieve pending messages
function getPendingMessages(callback) {
    db.all('SELECT * FROM messages_queue WHERE status = "pending"', [], (err, rows) => {
        if (err) {
            console.error('Error fetching pending messages:', err.message);
        } else {
            callback(rows);
        }
    });
}

// Update message status after sending
function updateMessageStatus(id, status) {
    const stmt = db.prepare('UPDATE messages_queue SET status = ? WHERE id = ?');
    stmt.run(status, id, (err) => {
        if (err) {
            console.error('Error updating message status:', err.message);
        } else {
            console.log(`Message status updated to ${status}.`);
        }
    });
    stmt.finalize();
}

module.exports = { addMessageToQueue, getPendingMessages, updateMessageStatus };
