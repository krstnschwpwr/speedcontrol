# Speed Ctrl

*short description*

![element 1](https://cloud.githubusercontent.com/assets/21247641/22448822/40f9013e-e75c-11e6-9261-71418fa98c19.png)


## ToDo

* [ ] Add development documentation
* [ ] Improve performance
* [ ] Enable app to run as different user
* [ ] Better [caddy](https://caddyserver.com/) installation

## Installation

> **IMPORTANT NOTICE**: All commands need to be executed as root (also the application).
> Currently it is not possible run the app as a different user but it is the next step on my roadmap.

```
curl https://my.secret.url.to.my.site/setup.sh | bash
```

1. Clone the git repository && setup required directories

```
$ cd /usr/local/
$ mkdir venvs
$ git clone https://github.com/krstnschwpwr/speedcontrol.git
$ cd speedcontrol
```

2. Install requirements & Caddy

```
$ apt install python3 python-pip python-dev sqlite3 ufw
$ virtualenv /usr/local/venvs/speedcontrol -p "$(which python3)"
$ source /usr/local/venvs/speedcontrol/bin/activate
$ pip install -r /usr/local/speedcontrol/requirements.txt
$ curl https://getcaddy.com | bash
``` 

3. Setup system service & configure system

```
$ cp /usr/local/speedcontrol/speedcontrol /etc/init.d/speedcontrol
$ chmod +x /etc/init.d/speedcontrol
$ systemctl daemon-reload
$ ufw enable && ufw allow ssh && ufw allow http
```

4. DONE!!! Start the service via `service speedcontrol start`

```
$ service speedcontrol [start|stop|restart]
```

## Important files

* Configuration files: `/usr/local/speedcontrol/speed_ctrl/settings.py`
* Log files: `/var/log/speedcontrol/{background|web}`.log
* PID files: `/var/run/speedcontrol-{web|background}.pid`

## License

See the included [LICENSE](LICENSE).

## Contribution Guidelines

*TBC*

## Development

*TBC*
