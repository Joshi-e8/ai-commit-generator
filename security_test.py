#!/usr/bin/env python3
"""
Security Testing Suite for Smart Commits AI
Tests for common vulnerabilities and security issues.
"""

import os
import sys
import tempfile
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any
import yaml
import re

class SecurityTester:
    """Security testing framework for Smart Commits AI."""
    
    def __init__(self):
        self.test_results = []
        self.temp_dirs = []
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all security tests."""
        print("🔒 Starting Security Test Suite")
        print("=" * 50)
        
        tests = [
            self.test_command_injection,
            self.test_path_traversal,
            self.test_api_key_exposure,
            self.test_file_permissions,
            self.test_input_validation,
            self.test_yaml_injection,
            self.test_dependency_vulnerabilities,
            self.test_information_disclosure
        ]
        
        for test in tests:
            try:
                result = test()
                self.test_results.append(result)
                self._print_test_result(result)
            except Exception as e:
                self.test_results.append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'message': str(e),
                    'severity': 'HIGH'
                })
        
        self._cleanup()
        return self._generate_report()
    
    def test_command_injection(self) -> Dict[str, Any]:
        """Test for command injection vulnerabilities."""
        print("\n🧪 Testing Command Injection...")
        
        # Create malicious repo path
        malicious_path = "/tmp/test; rm -rf /tmp/malicious; echo 'injected'"
        
        try:
            # This should fail safely
            from src.ai_commit_generator.config import Config
            config = Config(repo_root=Path(malicious_path))
            return {
                'test': 'command_injection',
                'status': 'VULNERABLE',
                'message': 'Command injection possible via repo_root',
                'severity': 'HIGH',
                'details': 'Malicious repo path accepted without validation'
            }
        except Exception:
            return {
                'test': 'command_injection',
                'status': 'SAFE',
                'message': 'Command injection prevented',
                'severity': 'INFO'
            }
    
    def test_path_traversal(self) -> Dict[str, Any]:
        """Test for path traversal vulnerabilities."""
        print("🧪 Testing Path Traversal...")
        
        # Create test directory
        test_dir = self._create_temp_git_repo()
        
        # Test malicious config file path
        malicious_config = test_dir / "../../../etc/passwd"
        
        try:
            # Create config with traversal path
            config_content = f"""
api:
  provider: groq
include: {malicious_config}
"""
            config_file = test_dir / ".commitgen.yml"
            config_file.write_text(config_content)
            
            from src.ai_commit_generator.config import Config
            config = Config(repo_root=test_dir)
            
            return {
                'test': 'path_traversal',
                'status': 'VULNERABLE',
                'message': 'Path traversal possible in config loading',
                'severity': 'HIGH',
                'details': 'Can access files outside repository'
            }
        except Exception:
            return {
                'test': 'path_traversal',
                'status': 'SAFE',
                'message': 'Path traversal prevented',
                'severity': 'INFO'
            }
    
    def test_api_key_exposure(self) -> Dict[str, Any]:
        """Test for API key exposure in logs/output."""
        print("🧪 Testing API Key Exposure...")
        
        test_dir = self._create_temp_git_repo()
        
        # Set fake API key
        os.environ['GROQ_API_KEY'] = 'sk-test123456789abcdef'
        
        try:
            from src.ai_commit_generator.config import Config
            config = Config(repo_root=test_dir)
            
            # Check if API key is exposed in string representation
            config_str = str(config.__dict__)
            if 'sk-test123456789abcdef' in config_str:
                return {
                    'test': 'api_key_exposure',
                    'status': 'VULNERABLE',
                    'message': 'API key exposed in object representation',
                    'severity': 'HIGH',
                    'details': 'API key visible in debug output'
                }
            
            # Test CLI output
            result = subprocess.run([
                sys.executable, '-m', 'src.ai_commit_generator.cli', 'config', '--show'
            ], cwd=test_dir, capture_output=True, text=True)
            
            if 'sk-test123456789abcdef' in result.stdout:
                return {
                    'test': 'api_key_exposure',
                    'status': 'VULNERABLE',
                    'message': 'API key exposed in CLI output',
                    'severity': 'HIGH',
                    'details': 'Full API key visible in config command'
                }
            
            return {
                'test': 'api_key_exposure',
                'status': 'SAFE',
                'message': 'API key properly masked',
                'severity': 'INFO'
            }
            
        except Exception as e:
            return {
                'test': 'api_key_exposure',
                'status': 'ERROR',
                'message': f'Test failed: {e}',
                'severity': 'MEDIUM'
            }
        finally:
            # Clean up environment
            if 'GROQ_API_KEY' in os.environ:
                del os.environ['GROQ_API_KEY']
    
    def test_file_permissions(self) -> Dict[str, Any]:
        """Test file permission security."""
        print("🧪 Testing File Permissions...")
        
        test_dir = self._create_temp_git_repo()
        
        try:
            from src.ai_commit_generator.git_hook import GitHookManager
            hook_manager = GitHookManager(repo_root=test_dir)
            
            # Install hook
            hook_manager.install_hook(force=True)
            
            # Check permissions
            hook_file = test_dir / ".git" / "hooks" / "prepare-commit-msg"
            if hook_file.exists():
                perms = oct(hook_file.stat().st_mode)[-3:]
                
                # Check if permissions are too permissive
                if perms in ['777', '776', '775', '774', '773', '772', '771']:
                    return {
                        'test': 'file_permissions',
                        'status': 'VULNERABLE',
                        'message': f'Hook file has overly permissive permissions: {perms}',
                        'severity': 'MEDIUM',
                        'details': 'Git hook file should have restrictive permissions'
                    }
                
                return {
                    'test': 'file_permissions',
                    'status': 'SAFE',
                    'message': f'Hook file has appropriate permissions: {perms}',
                    'severity': 'INFO'
                }
            
            return {
                'test': 'file_permissions',
                'status': 'ERROR',
                'message': 'Hook file not created',
                'severity': 'MEDIUM'
            }
            
        except Exception as e:
            return {
                'test': 'file_permissions',
                'status': 'ERROR',
                'message': f'Test failed: {e}',
                'severity': 'MEDIUM'
            }
    
    def test_input_validation(self) -> Dict[str, Any]:
        """Test input validation."""
        print("🧪 Testing Input Validation...")
        
        test_dir = self._create_temp_git_repo()
        
        try:
            from src.ai_commit_generator.core import CommitGenerator
            from src.ai_commit_generator.config import Config
            
            config = Config(repo_root=test_dir)
            generator = CommitGenerator(config)
            
            # Test malicious commit message
            malicious_messages = [
                "'; DROP TABLE commits; --",
                "<script>alert('xss')</script>",
                "../../../../etc/passwd",
                "\x00\x01\x02\x03",  # Null bytes
                "A" * 10000,  # Very long message
            ]
            
            vulnerabilities = []
            for msg in malicious_messages:
                try:
                    cleaned = generator._clean_message(msg)
                    if msg in cleaned or len(cleaned) > 1000:
                        vulnerabilities.append(f"Malicious input not sanitized: {msg[:50]}...")
                except Exception:
                    pass  # Expected to fail
            
            if vulnerabilities:
                return {
                    'test': 'input_validation',
                    'status': 'VULNERABLE',
                    'message': 'Input validation insufficient',
                    'severity': 'MEDIUM',
                    'details': vulnerabilities
                }
            
            return {
                'test': 'input_validation',
                'status': 'SAFE',
                'message': 'Input validation working correctly',
                'severity': 'INFO'
            }
            
        except Exception as e:
            return {
                'test': 'input_validation',
                'status': 'ERROR',
                'message': f'Test failed: {e}',
                'severity': 'MEDIUM'
            }
    
    def test_yaml_injection(self) -> Dict[str, Any]:
        """Test for YAML injection vulnerabilities."""
        print("🧪 Testing YAML Injection...")
        
        test_dir = self._create_temp_git_repo()
        
        # Malicious YAML content
        malicious_yaml = """
api:
  provider: groq
!!python/object/apply:os.system ["echo 'YAML injection successful'"]
"""
        
        try:
            config_file = test_dir / ".commitgen.yml"
            config_file.write_text(malicious_yaml)
            
            from src.ai_commit_generator.config import Config
            config = Config(repo_root=test_dir)
            
            return {
                'test': 'yaml_injection',
                'status': 'VULNERABLE',
                'message': 'YAML injection possible',
                'severity': 'HIGH',
                'details': 'Unsafe YAML loading allows code execution'
            }
            
        except yaml.constructor.ConstructorError:
            return {
                'test': 'yaml_injection',
                'status': 'SAFE',
                'message': 'YAML injection prevented by safe_load',
                'severity': 'INFO'
            }
        except Exception as e:
            return {
                'test': 'yaml_injection',
                'status': 'ERROR',
                'message': f'Test failed: {e}',
                'severity': 'MEDIUM'
            }
    
    def test_dependency_vulnerabilities(self) -> Dict[str, Any]:
        """Test for known dependency vulnerabilities."""
        print("🧪 Testing Dependency Vulnerabilities...")
        
        try:
            # Check if safety is available
            result = subprocess.run(['safety', '--version'], capture_output=True)
            if result.returncode != 0:
                return {
                    'test': 'dependency_vulnerabilities',
                    'status': 'SKIPPED',
                    'message': 'Safety tool not available',
                    'severity': 'INFO'
                }
            
            # Run safety check
            result = subprocess.run(['safety', 'check'], capture_output=True, text=True)
            
            if result.returncode != 0 and 'vulnerabilities found' in result.stdout.lower():
                return {
                    'test': 'dependency_vulnerabilities',
                    'status': 'VULNERABLE',
                    'message': 'Known vulnerabilities found in dependencies',
                    'severity': 'HIGH',
                    'details': result.stdout
                }
            
            return {
                'test': 'dependency_vulnerabilities',
                'status': 'SAFE',
                'message': 'No known vulnerabilities in dependencies',
                'severity': 'INFO'
            }
            
        except Exception as e:
            return {
                'test': 'dependency_vulnerabilities',
                'status': 'ERROR',
                'message': f'Test failed: {e}',
                'severity': 'MEDIUM'
            }
    
    def test_information_disclosure(self) -> Dict[str, Any]:
        """Test for information disclosure."""
        print("🧪 Testing Information Disclosure...")
        
        test_dir = self._create_temp_git_repo()
        
        try:
            # Test error messages
            from src.ai_commit_generator.core import CommitGenerator
            from src.ai_commit_generator.config import Config
            
            # Create invalid config
            config_file = test_dir / ".commitgen.yml"
            config_file.write_text("invalid: yaml: content: [")
            
            try:
                config = Config(repo_root=test_dir)
                return {
                    'test': 'information_disclosure',
                    'status': 'VULNERABLE',
                    'message': 'Invalid YAML accepted',
                    'severity': 'MEDIUM'
                }
            except Exception as e:
                error_msg = str(e)
                
                # Check if error message reveals sensitive information
                sensitive_patterns = [
                    r'/home/[^/]+',  # Home directory paths
                    r'/Users/[^/]+',  # macOS user paths
                    r'C:\\Users\\[^\\]+',  # Windows user paths
                    r'password',
                    r'secret',
                    r'key',
                ]
                
                for pattern in sensitive_patterns:
                    if re.search(pattern, error_msg, re.IGNORECASE):
                        return {
                            'test': 'information_disclosure',
                            'status': 'VULNERABLE',
                            'message': 'Error messages may reveal sensitive information',
                            'severity': 'MEDIUM',
                            'details': f'Pattern found: {pattern}'
                        }
                
                return {
                    'test': 'information_disclosure',
                    'status': 'SAFE',
                    'message': 'Error messages do not reveal sensitive information',
                    'severity': 'INFO'
                }
            
        except Exception as e:
            return {
                'test': 'information_disclosure',
                'status': 'ERROR',
                'message': f'Test failed: {e}',
                'severity': 'MEDIUM'
            }
    
    def _create_temp_git_repo(self) -> Path:
        """Create a temporary Git repository for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        self.temp_dirs.append(temp_dir)
        
        # Initialize Git repo
        subprocess.run(['git', 'init'], cwd=temp_dir, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=temp_dir)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=temp_dir)
        
        return temp_dir
    
    def _print_test_result(self, result: Dict[str, Any]) -> None:
        """Print test result with appropriate formatting."""
        status = result['status']
        test_name = result['test'].replace('_', ' ').title()
        
        if status == 'VULNERABLE':
            print(f"❌ {test_name}: {result['message']}")
        elif status == 'SAFE':
            print(f"✅ {test_name}: {result['message']}")
        elif status == 'ERROR':
            print(f"⚠️  {test_name}: {result['message']}")
        elif status == 'SKIPPED':
            print(f"⏭️  {test_name}: {result['message']}")
    
    def _cleanup(self) -> None:
        """Clean up temporary directories."""
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate security test report."""
        total_tests = len(self.test_results)
        vulnerable = len([r for r in self.test_results if r['status'] == 'VULNERABLE'])
        safe = len([r for r in self.test_results if r['status'] == 'SAFE'])
        errors = len([r for r in self.test_results if r['status'] == 'ERROR'])
        skipped = len([r for r in self.test_results if r['status'] == 'SKIPPED'])
        
        high_severity = len([r for r in self.test_results if r.get('severity') == 'HIGH'])
        medium_severity = len([r for r in self.test_results if r.get('severity') == 'MEDIUM'])
        
        print("\n" + "=" * 50)
        print("🔒 Security Test Report")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Safe: {safe}")
        print(f"❌ Vulnerable: {vulnerable}")
        print(f"⚠️  Errors: {errors}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"\n🚨 High Severity Issues: {high_severity}")
        print(f"⚠️  Medium Severity Issues: {medium_severity}")
        
        if vulnerable > 0:
            print(f"\n❌ SECURITY ISSUES FOUND - IMMEDIATE ACTION REQUIRED")
        else:
            print(f"\n✅ NO CRITICAL VULNERABILITIES DETECTED")
        
        return {
            'total_tests': total_tests,
            'vulnerable': vulnerable,
            'safe': safe,
            'errors': errors,
            'skipped': skipped,
            'high_severity': high_severity,
            'medium_severity': medium_severity,
            'results': self.test_results
        }

if __name__ == "__main__":
    tester = SecurityTester()
    report = tester.run_all_tests()
    
    # Exit with error code if vulnerabilities found
    if report['vulnerable'] > 0 or report['high_severity'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
