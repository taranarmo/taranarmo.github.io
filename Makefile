.PHONY: build serve clean nix-build nix-run

PORT ?= 8080

build:
	nix run .#build

serve:
	nix run

nix-build:
	nix build

clean:
	rm -rf result
