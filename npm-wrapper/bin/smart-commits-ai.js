#!/usr/bin/env node
/**
 * NPM wrapper for smart-commits-ai Python package
 * Forwards all commands to the Python CLI
 */

const { spawn } = require('cross-spawn');
const path = require('path');

function runSmartCommitsAI() {
    // Get command line arguments (excluding node and script name)
    const args = process.argv.slice(2);
    
    // Spawn the Python CLI with all arguments
    const child = spawn('smart-commits-ai', args, {
        stdio: 'inherit',
        cwd: process.cwd()
    });
    
    // Handle process exit
    child.on('close', (code) => {
        process.exit(code);
    });
    
    // Handle errors
    child.on('error', (error) => {
        if (error.code === 'ENOENT') {
            console.error('❌ smart-commits-ai not found!');
            console.error('');
            console.error('Please run the installation first:');
            console.error('  npm install smart-commits-ai');
            console.error('');
            console.error('Or install manually:');
            console.error('  pip install smart-commits-ai');
            process.exit(1);
        } else {
            console.error('❌ Error running smart-commits-ai:', error.message);
            process.exit(1);
        }
    });
}

// Run the CLI
runSmartCommitsAI();
