all:
	gcc generate.c -o inputGen -O3
clean:
	rm -f inputGen 