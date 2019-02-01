push: # build
	docker tag testok rzlatev/m2jk
	docker push rzlatev/m2jk

run: # build
	docker run -p 8890:8890 testok

build:
	cp ../demo/test.ipynb .
	cp ../demo/demo.ipynb .
	docker build --tag testok . --no-cache