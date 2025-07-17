#!/usr/bin/env node
/**
 * Installation script for smart-commits-ai NPM wrapper
 * Automatically installs the Python package via pip
 */

const { spawn } = require('cross-spawn');
const which = require('which');
const fs = require('fs');
const path = require('path');

class SmartCommitsInstaller {
    constructor() {
        this.packageName = 'smart-commits-ai';
        this.version = '1.0.4';
    }

    async checkPython() {
        console.log('🐍 Checking for Python installation...');
        
        const pythonCommands = ['python3', 'python'];
        
        for (const cmd of pythonCommands) {
            try {
                await which(cmd);
                console.log(`✅ Found Python: ${cmd}`);
                return cmd;
            } catch (error) {
                continue;
            }
        }
        
        throw new Error('Python not found. Please install Python 3.8+ from https://python.org');
    }

    async checkPip(pythonCmd) {
        console.log('📦 Checking for pip...');
        
        return new Promise((resolve, reject) => {
            const pip = spawn(pythonCmd, ['-m', 'pip', '--version'], { stdio: 'pipe' });
            
            pip.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ pip is available');
                    resolve();
                } else {
                    reject(new Error('pip not found. Please install pip.'));
                }
            });
        });
    }

    async installPackage(pythonCmd) {
        console.log(`🚀 Installing ${this.packageName} v${this.version}...`);
        
        return new Promise((resolve, reject) => {
            const install = spawn(pythonCmd, [
                '-m', 'pip', 'install', 
                `${this.packageName}==${this.version}`
            ], { 
                stdio: 'inherit' 
            });
            
            install.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Installation successful!');
                    resolve();
                } else {
                    reject(new Error('Installation failed'));
                }
            });
        });
    }

    async verifyInstallation() {
        console.log('🔍 Verifying installation...');
        
        return new Promise((resolve, reject) => {
            const verify = spawn('smart-commits-ai', ['--version'], { stdio: 'pipe' });
            
            let output = '';
            verify.stdout.on('data', (data) => {
                output += data.toString();
            });
            
            verify.on('close', (code) => {
                if (code === 0) {
                    console.log(`✅ Verification successful: ${output.trim()}`);
                    resolve();
                } else {
                    reject(new Error('Verification failed'));
                }
            });
        });
    }

    async install() {
        try {
            console.log('🤖 Smart Commits AI - NPM Installation');
            console.log('=====================================');
            
            const pythonCmd = await this.checkPython();
            await this.checkPip(pythonCmd);
            await this.installPackage(pythonCmd);
            await this.verifyInstallation();
            
            console.log('\n🎉 Installation Complete!');
            console.log('\nNext steps:');
            console.log('1. Navigate to your Git repository');
            console.log('2. Run: npx smart-commits-ai install');
            console.log('3. Add your API key to .env file');
            console.log('4. Start using AI-generated commit messages!');
            
        } catch (error) {
            console.error(`\n❌ Installation failed: ${error.message}`);
            console.error('\nTroubleshooting:');
            console.error('1. Ensure Python 3.8+ is installed');
            console.error('2. Ensure pip is available');
            console.error('3. Check your internet connection');
            process.exit(1);
        }
    }
}

// Run installation if this script is executed directly
if (require.main === module) {
    const installer = new SmartCommitsInstaller();
    installer.install();
}

module.exports = SmartCommitsInstaller;
