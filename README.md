## HEX Compiler

Create HEX files from INO/PDE files or project directories with Arduino CLI support.

## Compile Code

To compile, download the [source code](https://github.com/ATphonOS/ino_to_hex_compiler/archive/refs/heads/main.zip) and unzip it.

Option 1:

Compile command (create exe):
```Python
pyinstaller --onefile --windowed --icon=icon/logo_app.ico 
--add-data "icon;icon" --name "ATphonOS-INOtoHEXCompiler" main.py
```

Option 2:

Compile command (create a folder with the executable and all dependencies):

```Python
pyinstaller --onedir --windowed --icon=icon/logo_app.ico 
--add-data "icon;icon" --name "ATphonOS-INOtoHEXCompiler" main.py
```


## Usage


![inohex1](https://github.com/user-attachments/assets/9df40adf-612f-451c-9a52-3946e2d0b971)


1. Open the downloaded or compiled program.
2. Select a `.ino`/`.pde` file or a project folder.  
3. Download the executable version of [Arduino CLI](https://docs.arduino.cc/arduino-cli/installation/#latest-release) (no installation required). Extract the `.exe` file, insert the path to `arduino-cli.exe`, and save the configuration.  
4. Select the board: Arduino Uno, Arduino Mega, Arduino Leonardo, Arduino Nano, Arduino Micro, Arduino Pro Mini, or Arduino Yun.  
5. Press **Compile and Generate HEX**.  
6. The output displays process information and provides a link to the directory containing the generated files.  


![inotohex2](https://github.com/user-attachments/assets/ff7f545c-764a-4852-92ba-72c672a0521f)

7. The build directory contains the HEX file both with and without the bootloader for the selected board version.

![inotohex3](https://github.com/user-attachments/assets/d93c4667-bd51-435e-81e6-7e9d1b2e9fea)


[Arduino CLI repo](https://github.com/arduino/arduino-cli)

***Currently Windows-only***


