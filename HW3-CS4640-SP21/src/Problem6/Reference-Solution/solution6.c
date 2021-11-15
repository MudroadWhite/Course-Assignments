#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <assert.h>
#include <ctype.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "sort.h"


void
usage(char *prog) 
{
    fprintf(stderr, "usage: %s <-i file>\n", prog);
    exit(1);
}

int compare_function(const void * A, const void * B){
	rec_t *a, *b ; 
	a = (rec_t*) A ; b = (rec_t *) B ; 
	if(a->key < b->key) return -1; 
	else if(a->key > b->key) return 1 ; 
	else return 0 ; 	
}


int
main(int argc, char *argv[]){
    // arguments
    char *inFile = "/no/such/file";
    char *outFile = "/no/such/file"; 

    // input params
    int c;
    opterr = 0;
    while ((c = getopt(argc, argv, "i:o:")) != -1) {
			switch (c) {
				case 'i':
	    			inFile = strdup(optarg);
	    			break;
				case 'o':
	    			outFile = strdup(optarg);
	    			break;
	    			
			default:
	    		usage(argv[0]);
			}
    }

    // open input file 
    int fd = open(inFile, O_RDONLY);
    if (fd < 0) {
		perror("open-read");
		exit(1);
    }
    
    //input file size 
    struct stat buf;
	fstat(fd, &buf);
	int size = buf.st_size; 
   int numRecs = size/ sizeof(rec_t) ; 
   assert(sizeof(rec_t)==100) ; 	  	    
    
  
   rec_t r;
   int rc; 
   
   rec_t *allRecord = (rec_t*) malloc(numRecs * sizeof(rec_t)) ;  
	int i ; 
	for(i = 0 ; i < numRecs ; ++i)
	{
		rc = read(fd, &r, sizeof(rec_t));
		if (rc == 0) // 0 indicates EOF
	   	 break;
		if (rc < 0) {
	    	perror("read");
	    	exit(1);
		}
		allRecord[i] = r ; 	
	
	}      
   (void) close(fd);

	//sort values ... 
	qsort(allRecord, numRecs, sizeof(allRecord[0]), compare_function);

    //create output file 
   int outfd = open(outFile, O_WRONLY|O_CREAT|O_TRUNC, S_IRWXU);
   if (outfd < 0) {
		perror("open-write");
		exit(1);
   }

	for(i=0;i<numRecs;++i){
		rc = write(outfd, &allRecord[i], sizeof(rec_t))	;
		if (rc != sizeof(rec_t)) {
	   	perror("write");
	   	(void) close(outfd);
	    	exit(1);
		}
	}

	(void) close(outfd);
	  	
	free(allRecord) ; 

   return 0;
}

