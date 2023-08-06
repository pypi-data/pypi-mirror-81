svc-tracer
============================================================

Table of Contents
=================

- [About](#About)
- [Installing](#installing)
- [Usage](#Usage)

About
=====

svc-tracer is a command line tool based on scapy to trace service traffic, such as REST, thrift, .etc.

Installing
==========

- **Windows**

1. Install [Python 2.7 or 3.4+](https://www.python.org/):

    When installing, option **`Add python.exe to Path`** must be selected and enabled. Or after installation, manually add the Python installation directory and its Scripts subdirectory to your PATH. Depending on your Python version, the defaults would be C:\Python27 and C:\Python27\Scripts respectively.

1. Install the latest version of [Npcap](https://nmap.org/npcap/): 

    Default values are recommended. Scapy will also work with Winpcap.
    
1. Install `svc-tracer` via pip

    ```
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ svc-tracer
    ```

1. Reboot the system

- **Linux**

1. Install [Python 2.7 or 3.4+](https://www.python.org/)

1. Install [tcpdump](http://www.tcpdump.org/) and make sure it is in the $PATH

    ```
    # Debian/Ubuntu:
    sudo apt-get install tcpdump
    
    # Fedora:
    yum install tcpdump
    ```

1. Install `svc-tracer` via pip

    ```
    pip install -i https://mirrors.aliyun.com/pypi/simple/ svc-tracer
    ```

- **MacOSX**

1. Install [Python 2.7 or 3.4+](https://www.python.org/)

1. Install `libpcap`

    ```
    brew update
    brew install libpcap
    ```

1. Install `svc-tracer` via pip

    ```
    pip install -i https://pypi.douban.com/simple/ svc-tracer
    ```

- **Known Issues**

Refer [scapy install guide](https://scapy.readthedocs.io/en/latest/installation.html) for known problems.

Usage
=====

- **General command help**

    ```
    svc-tracer --help
    usage: svc-tracer [-h] {show,thrift,http} ...
    
    positional arguments:
      {show,thrift,http}
        show              Show all interfaces
        thrift            Trace thrift service
        http              Trace http service
    
    optional arguments:
      -h, --help          show this help message and exit
    ```

- **Command: show**
 
    Sub command `show` will show all available network interface's name in user's computer, so that they can use it as the parameter of `--iface`:

- **Command: http**
 
    Sub command `http` will trace http service requests and responses on specific network interface and specific port, command line help is below:

    ```
    svc-tracer http --help
    usage: svc-tracer http [-h] -i <iface> -p <port> [-f <ip> [<ip> ...]] [-t <ip> [<ip> ...]] [-m <regex> [<regex> ...]] [--unpaired]
                           [--print <mode>] [--check_interval <interval>] [--check_timeout <timeout>] [-l <level>] [-o <path>] [-c]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i <iface>, --iface <iface>
                            The interface of sniff from
      -p <port>, --port <port>
                            The port of the service listens to
      -f <ip> [<ip> ...], --from <ip> [<ip> ...]
                            Only record the messages from this IP(s)
      -t <ip> [<ip> ...], --to <ip> [<ip> ...]
                            Only record the messages to this IP(s)
      -m <regex> [<regex> ...], --method <regex> [<regex> ...]
                            Only record the messages match this method(s)
      --unpaired            Print the messages as they arrive, possibly out of order
      --print <mode>        Print parts of the message. Options: header, data, all, none
      --check_interval <interval>
                            Interval in seconds for checking unpair message
      --check_timeout <timeout>
                            Timeout in seconds for checking unpair alert
      -l <level>, --log-level <level>
                            The output level of messages. Options: debug, info, warn, error
      -o <path>, --log-file <path>
                            The output file of messages
      -c, --log-clear       The output file will be cleared
    ```

    - `iface`: **Required**. Specific the name of network interface, such as: `eth0`, ``  

    - `port`: **Required**. Specific the port of remote or local service listens to 
    
    - `from`: **Optional**. Make tracer only record the request from specific ip(s) and the response to specific ip(s). 
        
        Default: do not filter message by from ip.
    
    - `to`: **Optional**. Make tracer only record the request to specific ip(s) and from response to specific ip(s). 
    
        Default: do not filter message by to ip.

    - `method`: **Optional**. Make tracer only record the request and response with http url matching specific regex expression(s).
    
        Default: do not filter message by request url.

    - `unpaired`: **Optional**. This option will not pair the request and response, and print the message separately as they arrive. Note: possibly out of order because the pcap limitation.

        Default: Pair the request and response, and print them together.
    
    - `print`: **Optional**. This option will define the print parts of message. Options: `header`, `data`, `all`, `none`

        Default: `all`, print all parts of message.
    
    - `check_interval`: **Optional**. Tracer in `paired` mode will check the unpaired messages in queue for the specific interval. It is useful for finding requests without responses. This option will not work in `unpaired` mode.

        Default: 5 seconds.
    
    - `check_timeout`: **Optional**. Unpaired message's timeout value. Tracer will alert and print the timeout unpaired messages in `error` level. This option will not work in `unpaired` mode.

        Default: 5 seconds.
        
    - `log-level`: **Optional**. The output level of messages. Tracer will only print the messages with level higher than this level. 

        Default: `info`, print all messages.
        
    - `log-file`: **Optional**. The path of output file for messages.  

        Default: `None`, only output to console.
        
    - `log-clear`: **Optional**. Whether the output file will be cleared first.  

        Default: `false`, append to output file.

- **Command: thrift**
 
    Sub command `thrift` will trace thrift service requests and responses on specific network interface and specific port, command line help is below:

    ```
    svc-tracer thrift --help
    usage: svc-tracer thrift [-h] -i <iface> -p <port> [-f <ip> [<ip> ...]] [-t <ip> [<ip> ...]] [-m <regex> [<regex> ...]]
                             [--unpaired] [--print <mode>] [--check_interval <interval>] [--check_timeout <timeout>] [-l <level>]
                             [-o <path>] [-c] [--transport <trans>] [--protocol <proto>] [--finagle] [--idl-file <path>]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i <iface>, --iface <iface>
                            The interface of sniff from
      -p <port>, --port <port>
                            The port of the service listens to
      -f <ip> [<ip> ...], --from <ip> [<ip> ...]
                            Only record the messages from this IP(s)
      -t <ip> [<ip> ...], --to <ip> [<ip> ...]
                            Only record the messages to this IP(s)
      -m <regex> [<regex> ...], --method <regex> [<regex> ...]
                            Only record the messages match this method(s)
      --unpaired            Print the messages as they arrive, possibly out of order
      --print <mode>        Print parts of the message. Options: header, data, all, none
      --check_interval <interval>
                            Interval in seconds for checking unpair message
      --check_timeout <timeout>
                            Timeout in seconds for checking unpair alert
      -l <level>, --log-level <level>
                            The output level of messages. Options: debug, info, warn, error
      -o <path>, --log-file <path>
                            The output file of messages
      -c, --log-clear       The output file will be cleared
      --transport <trans>   Use a specific transport. Options: auto, buffered, framed
      --protocol <proto>    Use a specific protocol. Options: auto, binary, compact, json
      --finagle             Detect finagle-thrift traffic (i.e.: with request headers)
      --idl-file <path>     Use .thrift file to resolve types
    ```

    - `iface`: **Required**. Specific the name of network interface, such as: `eth0`, ``  

    - `port`: **Required**. Specific the port of remote or local service listens to 
    
    - `from`: **Optional**. Make tracer only record the request from specific ip(s) and the response to specific ip(s). 
        
        Default: do not filter message by from ip.
    
    - `to`: **Optional**. Make tracer only record the request to specific ip(s) and from response to specific ip(s). 
    
        Default: do not filter message by to ip.

    - `method`: **Optional**. Make tracer only record the request and response with http url matching specific regex expression(s).
    
        Default: do not filter message by request url.

    - `unpaired`: **Optional**. This option will not pair the request and response, and print the message separately as they arrive. Note: possibly out of order because the pcap limitation.

        Default: Pair the request and response, and print them together.
    
    - `print`: **Optional**. This option will define the print parts of message. Options: `header`, `data`, `all`, `none`

        Default: `all`, print all parts of message.
    
    - `check_interval`: **Optional**. Tracer in `paired` mode will check the unpaired messages in queue for the specific interval. It is useful for finding requests without responses. This option will not work in `unpaired` mode.

        Default: 5 seconds.
    
    - `check_timeout`: **Optional**. Unpaired message's timeout value. Tracer will alert and print the timeout unpaired messages in `error` level. This option will not work in `unpaired` mode.

        Default: 5 seconds.
        
    - `log-level`: **Optional**. The output level of messages. Tracer will only print the messages with level higher than this level. 

        Default: `info`, print all messages.
        
    - `log-file`: **Optional**. The path of output file for messages.  

        Default: `None`, only output to console.
        
    - `log-clear`: **Optional**. Whether the output file will be cleared first.  

        Default: `false`, append to output file.

    - `transport`: **Optional**. The transport frame mode of the thrift message.  

        Default: `auto`, auto detect the transport mode.

    - `protocol`: **Optional**. The protocol of the thrift message.  

        Default: `auto`, auto detect the protocol.

    - `finagle`: **Optional**. Try to detect finagle-thrift's request headers.  

        Default: `false`, auto detect the protocol.

    - `idl-file`: **Optional**. The path of .thrift file for resolving types of method's arguments.  

        Default: `None`, do not use .thrift file.
