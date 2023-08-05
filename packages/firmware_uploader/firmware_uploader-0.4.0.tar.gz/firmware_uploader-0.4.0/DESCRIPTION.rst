firmware_uploader_python
========================

Uploads firmware to multiple embedded devices.

Authors::

    Peter Polidoro <peterpolidoro@gmail.com>

License::

    BSD

Example Usage::

    fu -e teensy40 -d https://github.com/janelia-arduino/YArenaValveController "(/dev/ttyACM)[0-2]"
    # Environment: teensy40
    # Dry Run: True
    # Firmware URL: https://github.com/janelia-arduino/YArenaValveController
    # Upload ports: ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
    # Do you want to continue? [y/N]: y
    # Cloning into 'YArenaValveController'...
    #remote: Enumerating objects: 118, done.
    # remote: Counting objects: 100% (118/118), done.
    # remote: Compressing objects: 100% (78/78), done.
    # remote: Total 118 (delta 65), reused 88 (delta 35), pack-reused 0
    # Receiving objects: 100% (118/118), 19.79 KiB | 2.47 MiB/s, done.
    # Resolving deltas: 100% (65/65), done.
    # ['stty', '-F', '/dev/ttyACM0', '134']
    # ['pio', 'run', '-e', 'teensy40', '--target', 'upload', '--upload-port', '/dev/ttyACM0']
    # ['stty', '-F', '/dev/ttyACM1', '134']
    # ['pio', 'run', '-e', 'teensy40', '--target', 'upload', '--upload-port', '/dev/ttyACM1']
    # ['stty', '-F', '/dev/ttyACM2', '134']
    # ['pio', 'run', '-e', 'teensy40', '--target', 'upload', '--upload-port', '/dev/ttyACM2']

    fu -e teensy40 https://github.com/janelia-arduino/YArenaValveController "(/dev/ttyACM)[0-2]"
    # Environment: teensy40
    # Dry Run: False
    # Firmware URL: https://github.com/janelia-arduino/YArenaValveController
    # Upload ports: ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
    # Do you want to continue? [y/N]:

    fu -e teensy40 ./git/arduino/YArenaValveController/ "(/dev/ttyACM)[0-2]"
    # Environment: teensy40
    # Dry Run: False
    # Firmware URL: ./git/arduino/YArenaValveController/
    # Upload ports: ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
    # Do you want to continue? [y/N]:
