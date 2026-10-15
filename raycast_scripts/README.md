# Raycast Scripts

Scripts for raycast.

Scripts that need administrator privileges should use the macOS authorization
dialog instead of interactive `sudo`, since Raycast does not provide a terminal
for password entry. For example, `scripts/flush-dns.sh` uses:

```sh
/usr/bin/osascript -e 'do shell script "/usr/bin/dscacheutil -flushcache && /usr/bin/killall -HUP mDNSResponder" with administrator privileges'
```

macOS handles administrator credentials in its authorization dialog; the script
does not read or store the password. Keep privileged commands in a single call
and use `&&` between dependent commands. Exit on failure before printing a success
message, including when authorization is canceled.

See Apple's [`do shell script` reference](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/reference/ASLR_cmds.html).
