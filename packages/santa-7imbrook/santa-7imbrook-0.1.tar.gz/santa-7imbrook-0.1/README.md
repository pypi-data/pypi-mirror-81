Secret Santa
=============

Simple cli to match your friends or family up for secret santas!

Add people to your group, set a location to exclude households or partners. People in the same location wont get each other.

```shell
./santa.py add-person <name> <phone-number> <location>
```

You can test out your matches with `--dry-run`

```shell
./santa.py shuffle --dry-run
```

Then send it off! (without `--dry-run`) There's no way to track back who got who after the program quits so it's one shot.
