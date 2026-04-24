Internet breakout matrix


<img width="1800" height="886" alt="versa_internet_breakout_matrix" src="https://github.com/user-attachments/assets/5ac10906-9c26-43fa-bb70-788c5e312fe7" />

  Tests:

Dutch_Airways_Schiphol#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 14/260/1116 ms
Dutch_Airways_Schiphol#trace 8.8.8.8
Type escape sequence to abort.
Tracing the route to 8.8.8.8
VRF info: (vrf in name/id, vrf out name/id)
  1 10.20.10.1 8 msec 6 msec 1 msec
  2 192.168.101.5 10 msec 12 msec 4 msec
  3 192.168.101.6 5 msec 13 msec 2 msec
  4 192.168.88.1 3 msec 24 msec 6 msec
  5  *  *  *
  6  *  *  *
  7

            German_Airways_Schiphol
    
user@ubuntu2-desktop:~$ tracepath 8.8.8.8
 1?: [LOCALHOST]                      pmtu 1500
 1:  _gateway                         9.746ms
 1:  _gateway                         1.200ms
 2:  _gateway                         1.591ms pmtu 1371
 2:  192.168.101.5                    7.679ms
 3:  192.168.101.6                    4.339ms
 4:  192.168.88.1                     4.558ms
 5:  no reply
 6:  no reply
 7:  no reply
^C

            French_airways_schiphol

French_Airways_Schiphol#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 11/217/1032 ms
French_Airways_Schiphol#traceroute 8.8.8.8
Type escape sequence to abort.
Tracing the route to 8.8.8.8
VRF info: (vrf in name/id, vrf out name/id)
  1 10.20.30.1 12 msec 1 msec 1 msec
  2 192.168.101.10 6 msec 2 msec 1 msec
  3 192.168.88.1 2 msec 2 msec 1 msec
  4  *  *  *
  5  *  *

            Dutch_Airways_Frankfurt

Dutch_airways_frankfurt#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 12/217/1034 ms
Dutch_airways_frankfurt#trace
Dutch_airways_frankfurt#traceroute 8.8.8.8
Type escape sequence to abort.
Tracing the route to 8.8.8.8
VRF info: (vrf in name/id, vrf out name/id)
  1 10.30.10.1 8 msec 1 msec 1 msec
  2 192.168.101.5 24 msec 6 msec 3 msec
  3 192.168.101.6 7 msec 4 msec 3 msec
  4 192.168.88.1 2 msec 9 msec 4 msec
  5  *  *  *
  6  *  *  *
  7  *  *

            German_Airways_Frankfurt

user@ubuntu22-desktop:~$ tracepath 8.8.8.8
 1?: [LOCALHOST]                      pmtu 1371
 1:  _gateway                         5.462ms
 1:  _gateway                         0.998ms
 2:  192.168.101.5                    2.594ms
 3:  192.168.101.6                    4.098ms
 4:  192.168.88.1                     3.290ms
 5:  no reply
 6:  no reply
 7:  no reply
 8:  no reply
 9:  no reply
10:  no reply

            French_Airways_Frankfurt



French_Airways_Frankfurt#ping  8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 11/14/22 ms
French_Airways_Frankfurt#tr
French_Airways_Frankfurt#traceroute 8.8.8.8
Type escape sequence to abort.
Tracing the route to 8.8.8.8
VRF info: (vrf in name/id, vrf out name/id)
  1 10.30.30.1 2 msec 2 msec 0 msec
  2 192.168.101.14 2 msec 29 msec 3 msec
  3 192.168.88.1 3 msec 2 msec 2 msec
  4  *  *  *
  5  *  *
