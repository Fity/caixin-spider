help:
	@echo 'Makefile for caxin-spider'
	@echo '                         '
	@echo 'Usage:                   '
	@echo '    make db            init the postgresql database'
	@echo '    make test          run test cases'
	@echo '    make unittest      run unittest'
	@echo '    make dev           init a basic dev env'

clean:
	@echo 'meant to clear untracked files'

db:
	@echo 'meant to init database'

test:
	echo 'nothing now'


dev:
	pip install -r dev_requirements.txt
