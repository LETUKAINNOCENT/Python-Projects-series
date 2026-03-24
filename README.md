# 🐍 Python Multi-Version Environment Setup (pyenv + venv + VSCode)

This repository serves as a centralized workspace for managing multiple Python projects with different Python versions and dependencies.

---

## 📌 Why Use `pyenv` and Virtual Environments?

When working on multiple Python projects, you may encounter:

* Different required Python versions
* Conflicting package dependencies (e.g., different `numpy` versions)
* The need to test your code across multiple Python versions

To solve this:

* **`pyenv`** → Manages multiple Python versions
* **`venv`** → Creates isolated environments per project

Together, they ensure a clean, flexible, and reproducible development setup.

---

## ⚙️ Installing `pyenv`

### 🪟 Windows (pyenv-win)

1. Download: https://github.com/pyenv-win/pyenv-win

2. Create folder:

   ```powershell
   mkdir $HOME/.pyenv
   ```

3. Extract and copy files into `.pyenv`

4. Set environment variables:

   ```powershell
   [System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
   [System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
   ```

5. Add to PATH:

   ```powershell
   [System.Environment]::SetEnvironmentVariable('path',
   $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" +
   $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" +
   [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
   ```

6. Enable script execution (Admin PowerShell):

   ```powershell
   Set-ExecutionPolicy unrestricted
   ```

7. Test installation:

   ```powershell
   pyenv
   ```

---

### 🍎 macOS

Install dependencies:

```bash
xcode-select --install
brew install openssl readline sqlite3 xz zlib
```

Install pyenv:

```bash
brew install pyenv
```

Add to shell:

```bash
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
```

---

### 🐧 Linux (Ubuntu/Debian)

Install dependencies:

```bash
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
liblzma-dev python3-openssl git
```

Install pyenv:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Add to shell:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
```

---

## 🧠 Using `pyenv`

### Install Python versions

```bash
pyenv install 3.10.0
```

List available versions:

```bash
pyenv install -l
```

List installed versions:

```bash
pyenv versions
```

Check current version:

```bash
pyenv version
```

### Set Python versions

* Global (default):

```bash
pyenv global 3.10.0
```

* Per project:

```bash
pyenv local 3.10.0
```

* Temporary (session only):

```bash
pyenv shell 3.10.0
```

---

## 📦 Creating Virtual Environments (`venv`)

Inside your project directory:

1. Set Python version:

```bash
pyenv local 3.10.0
```

2. Create environment:

```bash
python -m venv .venv
```

3. Activate environment:

* macOS/Linux:

```bash
source .venv/bin/activate
```

* Windows:

```powershell
.\.venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install <package>
```

---

## 🧪 How It Works

* Each Python version is managed by `pyenv`
* Each project has its own `.venv`
* Dependencies are isolated per project
* No conflicts between projects 🎉

---

## 💻 VSCode Integration

To auto-activate your virtual environment:

1. Open Command Palette:

   ```
   Ctrl + Shift + P
   ```

2. Search:

   ```
   settings.json
   ```

3. Add:

   ```json
   {
     "python.terminal.activateEnvironment": true
   }
   ```

This ensures VSCode automatically activates `.venv` when you open the project.

---

## 🧹 Tips

* Always create a `.venv` per project
* Add `.venv/` to `.gitignore`
* Use `pyenv local` to lock project Python version
* Delete `.venv` anytime to reset your environment

---

## ✅ Summary

| Tool   | Purpose                         |
| ------ | ------------------------------- |
| pyenv  | Manage multiple Python versions |
| venv   | Isolate project dependencies    |
| VSCode | Seamless development experience |

---

## 🚀 Final Thoughts

Using `pyenv` + `venv` gives you:

* Clean environments
* Version flexibility
* Reproducible projects
* Zero dependency conflicts

Perfect setup for managing multiple Python projects in one repository.

---

