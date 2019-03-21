# scm
Simple Config Manager

### installation
`git clone` this repository.

install `sshpass` on the machine where you plan to execute the file `cm.py` (of course Python and a bunch of Python modules are required).

`bootstrap` the server you want to configure.

`configure` the server using the file `spec.txt` inside the `config/` directory.

NOTE: See below for an example of the `spec.txt` and a sample `.conf` file

This is a POC and the same configuration will be rendered for any machine!!!

### Bootstrap the target server (one time activity)
Run the command
```
# ./bootstrap.bash <SERVER_IP> init
```

### Sync the modules to the target server (needed if/when the 'execution' modules are modified)
Run the command
```
# ./bootstrap.bash <SERVER_IP>
```

### configure the server
Run the command
```
# python bin/cm.py <SERVER_IP>
```

This will print the commands to execute on screen.

For safety, these commands are not executed automatically, you can copy paste the `sshpass ...` lines for yourself.

### Example

The file `spec.txt` will be read line-by-line and configuration files inside `spec.txt` will be interpreted as actions to be performed on the target server.


File: spec.txt
```
install.conf
webserver.conf
```

File: install.conf (in the same directory as `spec.txt`)
```
[install_apache2]
action = "package.install"
name = "libapache2-mod-php5"
```

`install_apache2`: any free-form identifier
`action`: the syntax for this is `<module>`.`<function>`
Example: `package.install`, `package.remove`, `file.create`, etc.

`name`: `module` specific directives which will be interpreted by the module
For `package.install`, this will be the package name to be installed.
