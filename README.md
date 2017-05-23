# LED Distractions

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This collection of scripts are designed to drive a 12x12 matrix display for NeoPixels over a serial port, using an Ardunio. For full details, checkout [@edwardmccaughan's](https://github.com/edwardmccaughan) [rgb_led_control](https://github.com/edwardmccaughan/rgb_led_control) project.

## Table of Contents

 - [Background](#background)
 - [Install](#install)
   - [Dependencies](#dependencies)
   - [Running as a Service](#running-as-a-service)
 - [Usage](#usage)
 - [Building](#building)
 - [Maintainer](#maintainer)
 - [Contribute](#contribute)

## Background

[Ed](https://github.com/edwardmccaughan) built a 12x12 matrix display from NeoPixel LED strips. Together with the [CraftCodiness](https://github.com/craftcodiness) team, these scripts have been developed to display different patterns on the LED display. The scripts are packaged for Debian (all architectures), and have some Ruby and Python package dependencies. The Debian package automatically installs and enables a [systemd service](rcscripts/led-distractions.service) to run the visualisations on startup.

## Install

### Dependencies

Whether you are using the Debian package or running the scripts directly, you will need to install the Ruby and Python dependencies. The scripts depend on the [arduino-lights](https://github.com/craftcodiness/arduino-lights) project and a few other small python packages.

```
gem install arduino-lights
pip install -r requirements.txt
```

### Running as a Service

The project includes a [systemd unit file](rcscripts/led-distractions.service) that you can install to `/lib/systemd/system` on your systemd-enabled system. The Debian package will do this for you automatically.

If you are using `rvm` to manage your Ruby environment, you might need to create a global Gemset and link a wrapper script to `/usr/bin/ruby` to allow the service to find the correct version of ruby and its dependencies.

```
rvm install 2.4.0                                                    # Install Ruby
rvm gemset create ruby2.4.0@led-distractions                         # Create Gemset
rvm ruby2.4.0@led-distractions                                       # Use the Gemset
gem install arduino-lights                                           # Install the Gem
rvm alias create led-distractions ruby2.4.0@led-distractions         # Create an alias
rvm wrapper led-distractions led-distractions                        # Create a wrapper
ln -s /usr/local/rvm/wrappers/led-distractions/ruby /usr/bin/ruby    # Link the wrapper as default
```

Once the service file is registered, you should be able to enable the service with `systemctl enable led-distractions.service`.

## Usage

All of the scripts expect to render to the NeoPixel matrix display, connecting over a serial port which should be available at `/dev/ttyUSB0` by default. This can be overridden by setting the `BLEMU_DEVICE` environment variable. The scripts can work either with the device itself, or with an emulator. Check out the [arduino-lights](https://github.com/craftcodiness/arduino-lights) project for details of the display emulator.

The scripts can be run directly with python or ruby and in addition, the [led-distractions](led-distractions) wrapper script is provided which will look for scripts in the `/usr/share/led-distractions` folder and run one of them at random.

If [led-distractions](led-distractions) is run as a service on startup using the supplied [systemd unit file](rcscripts/led-distractions.service), each visualisation will run for a short period of time before the service is automatically restarted to trigger a different (or possibly the same) script.

## Building

Configuration files are supplied for Debian packaging. Use `debuild` to rebuild the package:

```
debuild --no-tgz-check
```

which will create appropriate architecture-independent Debian packages in the parent directory. When updating the package, us `dch` to update the changelog:

```
dch -v 0.0.3
```

## Maintainer

This code is maintained by the [CraftCodiness](https://github.com/craftcodiness) team.

## Contribute

Pull requests are more than welcome! We have very low standards.

## License

This code is licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl.txt), a [copy of which](LICENSE) is included in this repository.

Copyright CraftCodiness, 2017

