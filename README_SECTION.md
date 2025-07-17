# AI-Generated Commit Messages

This section demonstrates the power of AI-generated commit messages. When you make changes to your codebase, the AI analyzes the diff and generates a descriptive, conventional commit message.

## Examples

Here are some examples of AI-generated commit messages:

### Adding a New Feature
```diff
+function authenticateUser(token) {
+  const decoded = jwt.verify(token, process.env.SECRET_KEY);
+  return userService.findById(decoded.userId);
+}
```
**AI-Generated Message**: `feat(auth): add JWT token verification function`

### Fixing a Bug
```diff
-if (user.status = 'active') {
+if (user.status === 'active') {
   allowAccess();
}
```
**AI-Generated Message**: `fix(auth): correct assignment operator to comparison in user status check`

### Refactoring Code
```diff
-function processData(data) {
-  const result = [];
-  for (let i = 0; i < data.length; i++) {
-    result.push(transform(data[i]));
-  }
-  return result;
+function processData(data) {
+  return data.map(item => transform(item));
+}
```
**AI-Generated Message**: `refactor(utils): simplify data processing with map function`

## Benefits

- **Consistency**: All commit messages follow the same format
- **Descriptiveness**: AI understands the context of your changes
- **Time-Saving**: No need to think about what to write
- **Conventional**: Follows the conventional commits standard

Try it yourself by making changes and running `git commit`!

## Installation

To get started with AI-generated commit messages:

```bash
pip install smart-commits-ai
smart-commits-ai install
echo "GROQ_API_KEY=your_key_here" >> .env
```

Now every `git commit` will be enhanced with AI! 🚀
