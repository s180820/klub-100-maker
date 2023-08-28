venv:
	echo "Creating virtual environment..."
	python3 -m venv .venv

install:
	echo "Installing..."
	pip3 install --uprade pip
	pip3 install -r requirements.txt

clean:
	rm -rf .venv