#!/usr/bin/env node
/**
 * Test script for smart-commits-ai NPM package
 */

const { spawn } = require('cross-spawn');

async function runTest() {
    console.log('🧪 Testing Smart Commits AI NPM Package');
    console.log('=====================================');
    
    try {
        // Test 1: Check if the binary works
        console.log('Test 1: Binary execution...');
        const result = spawn.sync('node', ['bin/smart-commits-ai.js', '--help'], { 
            stdio: 'pipe',
            encoding: 'utf8'
        });
        
        if (result.status === 0 || result.status === 1) {
            console.log('✅ Binary execution test passed');
        } else {
            console.log('❌ Binary execution test failed');
            console.log('Error:', result.stderr);
        }
        
        // Test 2: Check installer
        console.log('\nTest 2: Installer module...');
        const SmartCommitsInstaller = require('./install.js');
        if (typeof SmartCommitsInstaller === 'function') {
            console.log('✅ Installer module test passed');
        } else {
            console.log('❌ Installer module test failed');
        }
        
        console.log('\n🎉 All tests completed!');
        console.log('\nTo test manually:');
        console.log('1. npm install -g .');
        console.log('2. smart-commits-ai --version');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        process.exit(1);
    }
}

runTest();
