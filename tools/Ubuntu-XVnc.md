# How to Setup Ubuntu 24.04 with XVnc

This guide provides step-by-step instructions to set up Ubuntu 24.04 with XVnc for remote desktop access.

## Prerequisites
- A system running Ubuntu 24.04.
- Basic knowledge of Linux command line.
- Access to a terminal with sudo privileges.

## Step 1: Update the System
```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Required Packages
```bash
sudo apt install -y xfce4 xfce4-goodies tigervnc-standalone-server tigervnc-common dbus-x11
```

## Step 3: Configure VNC Server

1. Create a new VNC configuration file:
   ```bash
   mkdir -p ~/.vnc
   nano ~/.vnc/xstartup
   ```
2. Add the following lines to the `xstartup` file:
   ```bash
   #!/bin/bash
   export DISPLAY=:2
   unset SESSION_MANAGER
   unset DBUS_SESSION_BUS_ADDRESS

   if command -v dbus-launch >/dev/null 2>&1; then
       eval "$(dbus-launch --sh-syntax --exit-with-session)"
   fi

   startxfce4 &
   ```
3. Make the `xstartup` file executable:
   ```bash
   chmod +x ~/.vnc/xstartup
   ```
   
4. Set a password for VNC access:
   ```bash
   vncpasswd
   ```
   
## Step 4: Start the VNC server:
   ```bash
   sudo vncserver :2 -geometry 1920x1200 -depth 24
   ```