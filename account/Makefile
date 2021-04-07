.PHONY: all

all: init plan apply plan-with-exit-code

init:
	@terraform14 init

plan:
	@terraform14 plan -out=plan.out
	@terraform14 show -json plan.out > plan.out.json

requested:
	@pipenv run python plan2event.py

created:
	@pipenv run python plan2event.py apply
