# Node JS

## Monorepo and Workspaces

This project uses a root-level `package.json` to manage all Node.js subprojects (workspaces) in a monorepo structure. The `workspaces` field in the root `package.json` lists all subprojects (e.g., `web/`).

**Example root package.json:**

```json
{
  "name": "tructrl-monorepo",
  "private": true,
  "version": "0.1.0",
  "workspaces": [
    "web"
  ]
}
```

## Installing Dependencies

Run the following command from the root of the workspace to install all dependencies for every workspace and create a single, shared `node_modules` directory:

```bash
npm install
```

This ensures all packages for all subprojects are installed and linked correctly. You do not need to run `npm install` in each subproject individually.

https://nodejs.org/en

## Install
```bash
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# In lieu of restarting the shell:
. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 22

# Verify the Node.js version:
node -v    # Should print "v22.17.0".
nvm current # Should print "v22.17.0".

# Verify npm version:
npm -v     # Should print "10.9.2".
```
