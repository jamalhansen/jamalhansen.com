---
alt: 'The Shell Switch Set Bash as your default terminal in VS Code — terminal showing:
  echo $SHELL'
author:
- Jamal Hansen
category:
- Blog Post
cover:
  alt: ''
  caption: ''
  image: 00b-vscode-default-shell-bash-image.jpg
  relative: true
date: 2026-05-12
draft: false
image_output:
- highlight: true
  text: /bin/bash
image_title: 'The Shell Switch

  Set Bash as your <em>default terminal</em> in VS Code'
series:
- Forging the Truth
slug: vscode-default-shell-bash
tags:
- vscode
- bash
- wsl
- shell-config
target_date: 2026-05-07
title: The Shell Switch
---

# The Shell Switch: Setting Your Native Tongue

## The Veil
When you open a terminal in VS Code, is it PowerShell blue? That default shell was chosen for you, not by you. The AI that's helping you code assumes Bash. If your terminal doesn't match, you're not building. You're translating.

## The Dross
The AI speaks Bash. Every path it gives you, every command it suggests, every script it writes -- Bash. When your terminal is PowerShell, every `/` becomes a `\` you have to fix by hand. You're spending mental energy on translation instead of on the problem.

## The Strike
Set Bash as your default terminal in VS Code.

1. Open the Terminal in VS Code.
2. Click the dropdown next to the `+` icon.
3. Select **"Select Default Profile"**.
4. Choose **Bash** (or WSL/Ubuntu).

Verify it worked:

```bash
echo $SHELL
```

You should see `/bin/bash`. If you do, the switch is done.

## The Truth
Consistency is infrastructure. When your terminal matches what the AI expects, its suggestions run the first time. You stop second-guessing whether a command failed because of the code or because of the shell. That's one less variable between you and knowing.

Next up: your terminal is set up. Now let's open a project in VS Code without touching the mouse.