const { spawn } = require('child_process');

// Spawn the Python process
const pythonProcess = spawn('python', ['./python/main.py']);

// Read from the console and write to the Python process
process.stdin.on('data', (data) => {
    pythonProcess.stdin.write(data);
});

// Read from the Python process and write to the console
pythonProcess.stdout.on('data', (data) => {
    process.stdout.write(data);
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
});