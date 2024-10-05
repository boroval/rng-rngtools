const fs = require('fs');
const MersenneTwister = require('./mersenne-twister'); // Include the RNG

// Command parsing function
function parseCommand(args) {
    let command = {};
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '-rw':
                command.writeSeed = true;
                break;
            case '-n':
                command.count = parseInt(args[++i]);
                break;
            case '-s':
                command.seed = parseInt(args[++i], 16); // Hexadecimal seed
                break;
            case '-r':
                command.range = parseInt(args[++i]);
                break;
            case '-f':
                command.outputFile = args[++i];
                break;
            case '-sf':
                command.seedFile = args[++i];
                break;
        }
    }
    return command;
}

// Function to generate the binary sequence
function generateBinarySequence(rng, count) {
    const byteCount = Math.ceil(count / 8); // Calculate the number of bytes
    let buffer = Buffer.alloc(byteCount); // Buffer to store binary data
    for (let i = 0; i < byteCount; i++) {
        let byte = 0;
        for (let bit = 0; bit < 8; bit++) {
            if (i * 8 + bit < count) {
                byte |= (rng.random_int() & 1) << (7 - bit); // Generate random bits and pack them into a byte
            }
        }
        buffer[i] = byte; // Store the byte in the buffer
    }
    return buffer;
}

// Function to generate a sequence of numbers within a range
function generateRangeSequence(rng, range, count) {
    let numbers = [];
    for (let i = 0; i < count; i++) {
        let number = Math.floor(rng.random() * range); // Generate a random number within the specified range
        numbers.push(number);
    }
    return numbers;
}

// Main function
function rngTool(args) {
    let command = parseCommand(args);
    let rng = command.seed ? new MersenneTwister(command.seed) : new MersenneTwister();

    // Write the seed file if required
    if (command.writeSeed && command.seedFile) {
        fs.writeFileSync(command.seedFile, `Seed: ${command.seed}`);
    }

    // Handle binary output
    if (command.outputFile.endsWith('.bin')) {
        let binaryData = generateBinarySequence(rng, command.count);
        fs.writeFileSync(command.outputFile, binaryData);
        console.log(`Binary file written to ${command.outputFile}`);
    } 
    // Handle text output for number sequences
    else if (command.outputFile.endsWith('.txt') && command.range !== undefined) {
        let numberSequence = generateRangeSequence(rng, command.range, command.count);
        fs.writeFileSync(command.outputFile, numberSequence.join('\n'));
        console.log(`Text file with number sequence written to ${command.outputFile}`);
    } 
    // Unsupported format
    else {
        console.log("Unsupported file format or missing parameters.");
    }
}

// Example usage
const args = process.argv.slice(2); // Get command-line arguments
rngTool(args);
