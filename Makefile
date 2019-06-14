.PHONY: build clean

MICROPYTHON-REPO=git@github.com:micropython/micropython.git
MICROPYTHON-COMMIT=14cf91f70467aa928f3e17223f108ace0864b4fe

build:
	git clone $(MICROPYTHON-REPO)
	cd micropython && git checkout $(MICROPYTHON-COMMIT)
	cd ../
	mkdir -p build
	cd micropython/ports/javascript/ && $(MAKE)
	cd ../../../
	cp micropython/ports/javascript/build/micropython.js build/
	cp micropython/ports/javascript/build/firmware.wasm build/
	patch -u build/micropython.js -i micropython.patch

clean:
	rm -rf micropython
	rm -rf build