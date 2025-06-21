import subprocess
import platform

if platform.system() == 'Windows':
    nw = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    print(nw.decode('ascii'))

elif platform.system() == 'Darwin':
    try:
        nw = subprocess.check_output(['airport', '-s'])
        print(nw.decode('utf-8'))
    except FileNotFoundError:
        print("❌ 'airport' command not found. Run this in terminal:\n"
              "sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport")

else:
    print("Unsupported OS")
