If you are using the OpenBCI with active electrodes you need to set the gain of the amplifier to work with them. To do this, enter this command:
```python
    python users.py -p deviceserialport
```

You should be greeted with a message that looks like this:

<img width="262" alt="image" src="https://user-images.githubusercontent.com/34819737/190931079-2078cc60-2b34-4bfd-a49e-09e8a2fb86d6.png">

Now enter the following codes into the console:
```python
    x1040010X
    x2040010X
    x3040010X
    x4040010X
    x5040010X
    x6040010X
    x7040010X
    x8040010X
```

Gain will now be changed, leave the setup tool:
```python
   /exit
```

Return to root folder of repo:
```python
   cd ..
```
