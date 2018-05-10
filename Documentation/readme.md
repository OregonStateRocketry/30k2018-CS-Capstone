# Setup Instructions:

## Clone SD Cards:
In Linux:

1. Without the SD card, on a host machine run `df -h` to see normal drives.

2. Insert the SD card into a USB reader, insert into the host and run `df -h` again.

   Notice there are new lines indicating your SD card, probably something like `/dev/sdb` or `/dev/sdb1` and `/dev/sdb2`.
  
   It's normal to have two or more lines if the SD card is already partitioned.

3. Copy the entire SD card into a file with `sudo dd if=/dev/sdb of=~/Downloads/sd_card_bu.img`

   The dd tool gives no progress bar or feedback, and you should understand it will take awhile because it copies the ENTIRE SD card, even blank space.

   So if you have a 16 GB SD card, your image will be 16 GB.

4. Remove the original (source) SD card and insert the new (target) SD card.

   Unmount the new SD card before writing to it:
   
   ```
   sudo umount /dev/sdb1
   sudo umount /dev/sdb2
   ```
   
   Write the image onto the target SD card:
   
   `sudo dd bs=4M if=~/Downloads/sd_card_bu.img of=/dev/sdb`
   
   Verify the write is complete:
   
   `sudo sync`
