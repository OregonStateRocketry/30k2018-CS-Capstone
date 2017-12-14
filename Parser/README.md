To run the parser script automatically on boot, copy esra-parser.service onto each of the Raspberry Pi Zeros (parsers) in /etc/systemd/system/ and run:

```
sudo systemctl start esra-parser
sudo systemctl enable esra-parser
```
