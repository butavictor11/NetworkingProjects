# Internet Breakout Validation

This section validates the internet breakout behavior for each airline tenant at both airport sites.

Dutch Airways and German Airways use **centralized internet breakout through the Brussels hub**.  
French Airways uses **local DIA breakout** directly from each airport site.

---

## Breakout Design Matrix

<img width="1800" height="886" alt="versa_internet_breakout_matrix" src="https://github.com/user-attachments/assets/0c4be8f4-e9ad-4695-b0ba-b47e2b31d1f1" />


---

## Validation Summary

| Tenant | Site | Ping to 8.8.8.8 | Traceroute Behavior | Result |
|---|---|---:|---|---|
| Dutch Airways | Schiphol | 100% success | Traffic follows the centralized breakout path through `192.168.101.5` and `192.168.101.6` before reaching `192.168.88.1` | Passed |
| German Airways | Schiphol | Reachable | Traffic follows the centralized breakout path through `192.168.101.5` and `192.168.101.6` before reaching `192.168.88.1` | Passed |
| French Airways | Schiphol | 100% success | Traffic exits locally through `192.168.101.10` before reaching `192.168.88.1` | Passed |
| Dutch Airways | Frankfurt | 100% success | Traffic follows the centralized breakout path through `192.168.101.5` and `192.168.101.6` before reaching `192.168.88.1` | Passed |
| German Airways | Frankfurt | Reachable | Traffic follows the centralized breakout path through `192.168.101.5` and `192.168.101.6` before reaching `192.168.88.1` | Passed |
| French Airways | Frankfurt | 100% success | Traffic exits locally through `192.168.101.14` before reaching `192.168.88.1` | Passed |

---

## Dutch Airways - Schiphol

**Expected behavior:** Centralized internet breakout through the Brussels hub.

```text
Dutch_Airways_Schiphol# ping 8.8.8.8

Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!

Success rate is 100 percent (5/5), round-trip min/avg/max = 14/260/1116 ms
```

```text
Dutch_Airways_Schiphol# traceroute 8.8.8.8

Tracing the route to 8.8.8.8

1  10.20.10.1       8 msec   6 msec   1 msec
2  192.168.101.5   10 msec  12 msec   4 msec
3  192.168.101.6    5 msec  13 msec   2 msec
4  192.168.88.1     3 msec  24 msec   6 msec
5  *  *  *
6  *  *  *
```

**Result:** Passed. Traffic follows the centralized breakout path.

---

## German Airways - Schiphol

**Expected behavior:** Centralized internet breakout through the Brussels hub.

```text
German_Airways_Schiphol$ tracepath 8.8.8.8

1?: [LOCALHOST]        pmtu 1500
1:  _gateway           9.746ms
1:  _gateway           1.200ms
2:  _gateway           1.591ms pmtu 1371
2:  192.168.101.5      7.679ms
3:  192.168.101.6      4.339ms
4:  192.168.88.1       4.558ms
5:  no reply
6:  no reply
7:  no reply
```

**Result:** Passed. Traffic follows the centralized breakout path.

---

## French Airways - Schiphol

**Expected behavior:** Local DIA breakout from Schiphol.

```text
French_Airways_Schiphol# ping 8.8.8.8

Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!

Success rate is 100 percent (5/5), round-trip min/avg/max = 11/217/1032 ms
```

```text
French_Airways_Schiphol# traceroute 8.8.8.8

Tracing the route to 8.8.8.8

1  10.20.30.1       12 msec   1 msec   1 msec
2  192.168.101.10    6 msec   2 msec   1 msec
3  192.168.88.1      2 msec   2 msec   1 msec
4  *  *  *
5  *  *
```

**Result:** Passed. Traffic exits locally through the Schiphol DIA path.

---

## Dutch Airways - Frankfurt

**Expected behavior:** Centralized internet breakout through the Brussels hub.

```text
Dutch_Airways_Frankfurt# ping 8.8.8.8

Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!

Success rate is 100 percent (5/5), round-trip min/avg/max = 12/217/1034 ms
```

```text
Dutch_Airways_Frankfurt# traceroute 8.8.8.8

Tracing the route to 8.8.8.8

1  10.30.10.1       8 msec   1 msec   1 msec
2  192.168.101.5   24 msec   6 msec   3 msec
3  192.168.101.6    7 msec   4 msec   3 msec
4  192.168.88.1     2 msec   9 msec   4 msec
5  *  *  *
6  *  *  *
7  *  *
```

**Result:** Passed. Traffic follows the centralized breakout path.

---

## German Airways - Frankfurt

**Expected behavior:** Centralized internet breakout through the Brussels hub.

```text
German_Airways_Frankfurt$ tracepath 8.8.8.8

1?: [LOCALHOST]        pmtu 1371
1:  _gateway           5.462ms
1:  _gateway           0.998ms
2:  192.168.101.5      2.594ms
3:  192.168.101.6      4.098ms
4:  192.168.88.1       3.290ms
5:  no reply
6:  no reply
7:  no reply
8:  no reply
9:  no reply
10: no reply
```

**Result:** Passed. Traffic follows the centralized breakout path.

---

## French Airways - Frankfurt

**Expected behavior:** Local DIA breakout from Frankfurt.

```text
French_Airways_Frankfurt# ping 8.8.8.8

Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!

Success rate is 100 percent (5/5), round-trip min/avg/max = 11/14/22 ms
```

```text
French_Airways_Frankfurt# traceroute 8.8.8.8

Tracing the route to 8.8.8.8

1  10.30.30.1       2 msec   2 msec   0 msec
2  192.168.101.14   2 msec  29 msec   3 msec
3  192.168.88.1     3 msec   2 msec   2 msec
4  *  *  *
5  *  *
```

**Result:** Passed. Traffic exits locally through the Frankfurt DIA path.

---

## Conclusion

The tests validate that the SD-WAN internet breakout policy works as designed:

- Dutch Airways uses centralized breakout through the Brussels hub.
- German Airways uses centralized breakout through the Brussels hub.
- French Airways uses local DIA breakout at each airport.
- Internet reachability was successful from all tenant/site combinations.
- Traceroute and tracepath output confirm that each tenant follows the expected breakout model.
