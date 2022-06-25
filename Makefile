SHELL=/bin/bash
run:
	source ~/envs/entry_notification/bin/activate; \
	nohup python main.py &
check:
	ps aux | grep "main.py"
