# StreamChecker

Simple tool that filters from your follows text file the Twitch streams that
are online. CLI tool allows choosing stream to start from follows that are
online.

[Usage][4] `streamchecker -l` to output links of streams that are online.


### Requirements

* Python 3.8 or newer
  * In Ubuntu `sudo apt install python3`
  * In Windows install [Python 3](https://www.python.org/)
    * You should consider selecting `Add Python to PATH` during install


### Install

1.  Install [Python 3](https://www.python.org/) from the [Requirements][1]
2.  Run `pip install streamchecker` to install from [PyPI][3]
3.  Run `streamchecker -v` to show installed streamchecker version number
4.  Create your streamer list [Configuration][2]


### Configuration

Add "streamer name" into your follows csv file. Separate each streamer with a
comma.

**Linux:** `~/.config/streamchecker/follows.csv`

**Windows:** `%USERPROFILE%\Documents\streamchecker\follows.csv`

The "streamer name" can be found at the end of a Twitch link:
`https://www.twitch.tv/<streamer_name>`

**follows.csv**
```
esamarathon,gamesdonequick,esl_csgo
```


##### CLI Play

Add your player of choice to CLI configuration file.

**Linux:** `~/.config/streamchecker/cli.json`

**Windows** `%USERPROFILE%\Documents\streamchecker\cli.json`

**cli.json**
```
{"player": ["/usr/bin/mpv", "--terminal-no"]}
```


### Usage

* `streamchecker -h` to list all possible arguments
* `streamchecker -v` to show installed streamchecker version
* `streamchecker -c` output follows that are streaming
* `streamchecker -l` output links of follows that are streaming
* `streamchecker -d` output displaynames of follows that are streaming
* `streamchecker -p` output online streams and choose one to play
  * Requires setting your player of choice [CLI Config][5]


[1]: #requirements
[2]: #configuration
[3]: https://pypi.org/project/streamchecker
[4]: #usage
[5]: #cli-play
