#!/usr/bin/env python3

import configparser
import PIL.Image


def load_config():
    config = configparser.ConfigParser()
    config.read('config.cf')
    return config['Resizer']


def main():
    config = load_config()
    img = PIL.Image.open(config["path"])
    height = int(config["height"])
    width = int(img.size[0] * (height / img.size[1]))
    img = img.resize((width, height), PIL.Image.ANTIALIAS)
    img.save(config["path"])


if __name__ == '__main__':
    main()
