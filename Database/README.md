To run the monitoring script automatically on boot, copy esra-monitor.service onto the Raspberry Pi 3 (host) in /etc/systemd/system/ and run:

```
sudo systemctl start esra-monitor
sudo systemctl enable esra-monitor
```

The parser is also running as a daemon.  The file is `/etc/systemd/system/esra-parser.service`

```
sudo systemctl start esra-parser
sudo systemctl enable esra-parser
```
