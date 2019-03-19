# scm
Simple Config Manager

# Installation
`git clone` this repository.

install `sshpass` on the machine where you plan to execute the file `cm.py` (of course Python and a bunch of Python modules are required).

`bootstrap` the server you want to configure.

`configure` the server using the file `spec.txt` inside the `config/` directory.

This is a POC and the same configuration will be rendered for any machine!!!

# bootstrapping the server for the first time
Run the command
```
# ./bootstrap.bash <SERVER_IP> init
```

# syncing the modules to the server
Run the command
```
# ./bootstrap.bash <SERVER_IP>
```

# configure the server
Run the command
```
# python bin/cm.py <SERVER_IP>
```

This will print the commands to execute on screen.

For safety, these commands are not executed automatically, you can copy paste the `sshpass ...` lines for yourself.
