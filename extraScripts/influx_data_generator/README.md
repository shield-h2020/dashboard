# InfluxDB Data generator

This script intends to generate attack data for InfluxDB in SHIELD's context.
It gives the user the chance to choose how many data will be generated, the attack type and severity and even the destination IPs.

The script currently uses the CSV format format:
```
timereceived,Year,Month,Day,hour,minutes,seconds,duration,src_ip,dst_ip,s_port,d_port,protocol,in_pkt,in_bytes,out_pkts,out_bytes,score
2018-08-14 11:26:08	2018	6	8	14	30	18	45	194.177.211.146	10.101.30.60	443	50228	TCP	2	104	0	0	0.000132496798604
```

The final result of the Generator is something similar to:

```
0001	High	Slowloris	2018-08-14 18:18:46	2018	6	8	14	51	38	0	67.195.83.30	10.101.30.60	443	3412	TCP	1	40	0	0	0.000300027351243
```

## Install Script

In order to install the requirements it's recommended the usage of a virtualenv

### VirtualEnv

```
$ sudo apt-get install virtualenv
```

To create and activate a new virtualenv just run the following command:

```
$ virtualenv -p python3 envname
$ source envname/bin/activate
```

## Requirements

Currently the script only needs pika library as external requirement, however it's listed on a requirements.txt file. To install it use:

```
$ pip install -r requirements.txt
```

## Script Usage

The script has a help method that can be acceded with:

```
$ python rmq_sender.py -h
```

IMPORTANT: Until the SHIELD user has not define custom IP associations only use the default **-i 10.101.30.60** otherwise there will be an association error!

### Examples

Generate 24 attacks starting on date 2018-08-20 separated by 60 minutes with destination IPs 192.168.1.1, 192.168.1.2

```
python rmq_sender.py --e 24 -d 2018-08-20 -j 60 -i "192.168.1.1, 192.168.1.2" -t "DoS"
```