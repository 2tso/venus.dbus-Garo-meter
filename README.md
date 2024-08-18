A try to add the Garo energymeter GNM3D-LP to venus OS.
Seems to work now but cgwacs needs to be disbled by editing /etc/venus/serial-starter.py as it detects the meter.
However, the get_ident method may need to be modified if the /var/log/dbus-modbusclient log shows a method that throw exception caused by null characters in string

