# ModbusScanner

A multi process scanner for checking ICS whether is readable. You can use this with MASSCAN or ZMap to check all the vulnerable ICS in IPv4 space. Notice that, it's better to use slow TCP scan if you're making a professional penetration test.

## Dependencies

That's easy, just run :

```
pip install pymodbus
```

## Usage

Put IP address list to a file named scan, then modify the port in the script, run it.
