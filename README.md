# Wokwi Platform.io Bridge Example

Note: this is an early prototype, and the implementation is subject to change without notice. Future versions may also impose limits and restrictions on the usage of this feature.

For questions use the Wokwi discord chat at https://wokwi.com/discord

## Usage

1. Install Python version 3.8 or newer and the PlatformIO CLI.
2. Install the python requirements by running
   
   ```
   pip install -r requirements.txt
   ```
3. Build the sample arduino project by running
   ```
   cd example && pio run
   ```
4. Start the bridge server
   ```
   python server.py
   ```
5. Open the following link in your web browser:
   
   https://wokwi.com/_alpha/wembed/335697688728175187?partner=platformio&port=9012&data=demo"

   You can change the number in the link to any valid Wokwi project id. The simulator will use the
   given project as a template for the diagram (and possibly other settings, such as SD Card files).

## Customization and debugging

You can modify the hex/elf file paths inside server.py to serve different set of files.

The bridge server also opens a local GDB server at port 9333. You can debug the code running in the simulation by attaching GDB to this port:

```
target remote localhost:9333
```
