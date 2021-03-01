# vcokltfre/PinManager

## A Discord bot that automatically managed your channel pins

This is a super simple bot which managed your channel pins. When a channel reaches 50 pins it takes the oldest pin and reposts it in an archive channel with a jump link.

To add an archive channel for a channel: `p!pins add <channel> <archive_channel>`

To remove an archive channel for a channel: `p!pins del <channel>`

That's all there is to it!

## Setup:

- You will need Python installed
- Run `pip install -r requirements.txt` (`pip3` on Linux)
- Copy `.env.example` to `.env` and fill in your token
- Done!
