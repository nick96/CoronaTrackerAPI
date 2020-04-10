
up:
	docker-compose up -d

test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build --exit-code-from test db test

push:
	heroku container:push web

deploy: push
	heroku container:release web
