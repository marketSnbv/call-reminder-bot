# call-reminder-bot
Chooses who will call today and reminds to do it.

To run this needs two config files. First - "who.txt". This can be blank, it will be updated automatically by bot. Second - "who_calls.txt" contains information about number of round, participants and how many times they were chosen. This information also will be updated automatically.

Example of "who_calls.txt":
1 (number of call)
@qwe 0
@asd 0
@zxc 0

Bot chooses who will call at a time specified in scheduling() function and reminds before calling. Also caller can be rerolled using "/choose" command. To check who is chosen and when this information was updated you can use"/check" command.
