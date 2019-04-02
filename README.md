# badges

Repository to create badges for the attendees of conference/workshop. The process is described in details at https://bioinfoexpert.com/?p=907

```bash
# if you need to generate random passwords
./get_usernames.py participants.txt

# generate pdf with badges - it'll be saved as badges.svg.pdf
./tsv2badges.py badges.svg participants.txt.badges.tsv
# clean-up
rm badges.svg*svg.pdf

# you can create user accounts easily if needed
while read line; do if [ ! -d `echo $line | cut -f6 -d":"` ]; then echo $line; echo $line | sudo newusers; fi; done < participants.txt.newusers
```

## Dependencies
```bash
sudo apt install inkscape
```