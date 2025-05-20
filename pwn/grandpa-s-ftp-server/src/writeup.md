# Grandpa's FTP Server

Name: `Grandpa's FTP Server`

Description:
```
My grandpa asked me to help him add the newest technology to his home server. When I asked him what that meant, he said I should add an FTP server so he can more easily reach his files.
I've managed to set it up, but he insisted that I integrate it with his existing authentication server. That server is one of the slowest things I have ever seen!
Logging in to the server takes forever because of this! Anyway, it's done, so he can go enjoy his files now.

PS: due to technical restrictions, usernames and password can only contain upper- or lower case letters, digits, underscores and dashes. The flag format is Trojan{username:password}
```

Along with the description, a FTP command is provided: `ftp grandpa-chall.trojanc.tf`. Trying this prompts us to log in with a username, and most commands seem to give an error message. Therefore, it seems the only way is to log in. 

The description mentions that the authentication is handled by an old and slow authentication server, so it's possible that the username and password checking is done very slowly. This opens up the door for a timing-based side channel attack.

Side channel attacks utilize not only the direct output of a program, but also additional information from so-called side channels. One of these side channels is timing: how quickly a computer can perform some program execution may be influenced by the details of the data that that program is handling.

In our case, this could mean that the timing of the username and password check could be a side channel, as slow execution amplifies the timing, making it easier to measure.

Before we continue, it's good to understand how string comparison is typically implemented. In higher-level languages, one can simply write `s1 == s2`, but there is actually something happening with such a statement under the hood. Specifically, most of these typically iterate through each character of the string from the start, and if there's ever two characters that aren't equal, false is returned. If all characters matched, the strings are equal. 

> Note that in lower-level languages, you should take proper care that you don't read out of the memory bounds of the string, e.g. for null-terminated strings.

Now, consider the timing of such an algorithm: if the first characters of the two strings are not equal, such as with `s1 = "abc", s2 = "def"`, then false is returned almost immediately! If instead the loop iterated a couple more times, such as for `s1 = "helpme", s2 = "hello"`, then the loop takes a little while longer to execute.

Such differences in running times can be difficult to measure on modern hardware, which can perform billions of operations per second. Furthermore, the instability of an internet connection to the server poses a challenge as well, as the communication to the server also takes some time. Furthermore, the time this communication takes is likely not constant, and will vary over time.

Luckily, our FTP server's string comparison may be running on 'old hardware', and thus could be very slow! Therefore, it's worth checking this approach out further. Writing a small script that checks each single-character username reveals that indeed, the character `g` takes 0.2 seconds longer than the other characters. With this principle in mind, we can build up our username character by character. Each time we find a character that takes significantly longer than the others, we append it to the username. Due to the varying delays from the communication over the internet, we keep trying the characters that take over 0.2 seconds extra, in case there are multiple. This way we can distinguish the communication delay from the hardware delay.

You can find a solve script in `ftp_solve2.py`, which implements this behaviour. It builds up the username and password character by character, by checking if the delay increases by 0.2 seconds for each new character. Furthermore, if it finds multiple characters with sufficient delay increase, it will keep trying with all of them until only one remains.

Running this finds the username `gRamP5` and password `iS_C0ol`, forming the flag `Trojan{gRamP5:iS_C0ol}`