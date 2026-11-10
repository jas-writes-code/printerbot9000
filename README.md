# printerbot9000
surprisingly simple discord bot that connects to escpos printer

**Setup:**
* `git clone` the repository
* `pip install -r requirements.txt`
* go into config.json and fill out:
*   your discord bot token
*   your printer model according to [this list](https://python-escpos.readthedocs.io/en/latest/printer_profiles/available-profiles.html)
*   the usb location of your printer from `lsusb`
*   the max characters your printer fits on a single line. this is usually either a google or testing thing so that's up to you really
