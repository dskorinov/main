# DESCRIPTION

telegram bot, in progress

## Build and run

1. clone repo 

```

git clone https://github.com/dskorinov/main.git

```

2. change directory

```

cd ./main/telegram/checker

```

3. rename config file

```

mv example.cfg config_checker.cfg

```

4. don't forget about bot token:
- as env variable (-e BOT_TOKEN=your_token)
- as env-file variable (--env-file=path/to/file with BOT_TOKEN=your_token)
- change config file variable

5. build docker

```

./build.sh

```
6. check run_bot.sh, change if needed

```

./run_bot.sh

```
